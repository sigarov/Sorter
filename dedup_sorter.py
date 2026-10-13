"""DedupSorter-Thread: entfernt/verschiebt _1, _2-Duplikate im Zielordner."""

import os
import re
import shutil
from datetime import datetime

from config import DUPES_FOLDER
from utils import dry_log_pfad, hash_datei
from worker_base import MediaWorker


class DedupSorter(MediaWorker):
    """Verschiebt NAME_1.jpg, NAME_2.jpg, ... im Zielordner nach Duplicates.

    Der Lauft arbeitet ausschliesslich im **Zielordner** des Sortierlaufs –
    dort entstehen die _1, _2-Dateien bei Namensgleichheit.

    Standard (force=False): nur behandeln, wenn byte-identisch zu NAME.jpg.
    force=True          : ALLE _1, _2, ... behandeln, egal ob der Inhalt
                          abweicht.
    Fehlt NAME.jpg, wird NAME_1.jpg in NAME.jpg umbenannt.
    Fehlt die Basisdatei, wird auch eine einzelne _1-Datei in den
    Basisnamen umbenannt und bleibt im Zielordner.
    Es wird nichts geloescht: die Duplikate landen in <Ziel>/Duplicates/<rel>
    und koennen dort spaeter manuell geprueft werden. Der Keeper wird einmal
    pro Gruppe mit hineinkopiert, damit sich die Dateien vergleichen lassen."""

    SUFFIX_RE = re.compile(r"^(?P<base>.+)_(?P<num>\d{1,2})$")

    def __init__(self, ziel, trockenlauf, force, lang, log_queue, stop_event):
        # Ein einziger Wurzelordner (das Ziel), keine Ordnerfilter.
        super().__init__(ziel, "", [], [], lang, log_queue, stop_event)
        self.ziel = os.path.abspath(ziel)
        self.trockenlauf = trockenlauf
        self.force = force
        self.stat = {
            "verschoben": 0,
            "keeper_kopiert": 0,
            "behalten": 0,
            "unterschiedlich": 0,
            "fehler": 0,
            "gruppen": 0,
            "umbenannt": 0,
            "force_geloescht": 0,
            "gesamt": 0,
        }
        self.pro_ordner = {}
        self._dry_log = None
        self._dry_log_path = None
        self.copied_keepers = set()

    def melde(self, text, tag="info"):
        """Wie in der Basisklasse, zusaetzlich ins Trockenlauf-Log schreiben."""
        super().melde(text, tag)
        if self._dry_log is not None:
            try:
                self._dry_log.write(f"{text}\n")
                self._dry_log.flush()
            except Exception:
                pass

    def _melde_fortschritt(self, idx, total):
        """Meldet den Fortschritt gedrosselt (alle 10 Dateien und am Ende)."""
        self.melde_fortschritt(
            idx,
            total,
            "log_dedup_progress",
            verschoben=self.stat["verschoben"],
            behalten=self.stat["behalten"],
            umbenannt=self.stat["umbenannt"],
            verschieden=self.stat["unterschiedlich"],
        )

    def gruppiere(self, alle):
        gruppen = {}
        for p in alle:
            d = os.path.dirname(p)
            name = os.path.basename(p)
            stem, ext = os.path.splitext(name)
            m = self.SUFFIX_RE.match(stem)
            if m:
                base_stem = m.group("base")
                num = int(m.group("num"))
            else:
                base_stem = stem
                num = 0
            key = (d.lower(), base_stem.lower(), ext.lower())
            gruppen.setdefault(key, []).append((p, num))
        return gruppen

    def _dupes_dst(self, src_path):
        """Zielpfad <Ziel>/Duplicates/<relativer Pfad>."""
        try:
            rel = os.path.relpath(os.path.abspath(src_path), self.ziel)
        except Exception:
            return None
        if rel.startswith(".."):
            return None
        return os.path.join(self.ziel, DUPES_FOLDER, rel)

    @staticmethod
    def _unique_path(path):
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        n = 1
        while os.path.exists(f"{base}_{n}{ext}"):
            n += 1
        return f"{base}_{n}{ext}"

    @staticmethod
    def _relevante_gruppen(gruppen):
        """Gruppen, die bearbeitet werden.

        Mehr als eine Datei bedeutet Duplikat-Kandidat. Eine einzelne Datei
        mit Nummer (_1, _2, ...) wird ebenfalls aufgenommen, damit sie in den
        Basisnamen umbenannt wird, wenn die Basisdatei fehlt."""
        return {k: v for k, v in gruppen.items() if len(v) > 1 or v[0][1] > 0}

    def run(self):
        try:
            if self.trockenlauf:
                dry_path = dry_log_pfad(self.ziel)
                try:
                    self._dry_log = open(dry_path, "w", encoding="utf-8")
                    self._dry_log_path = dry_path
                    self._dry_log.write(self.T("log_start_header", zeit=datetime.now()) + "\n")
                except Exception:
                    self._dry_log = None

            self.melde(self.T("log_dedup_ziel", path=self.ziel))
            alle = self.sammle_dateien()
            self.stat["gesamt"] = len(alle)
            self.melde(self.T("log_found_sources", n=len(alle)))

            if self.trockenlauf:
                self.melde(self.T("log_dryrun_mode"), "warn")
                if self._dry_log_path is not None:
                    self.melde(self.T("log_drylogfile", path=str(self._dry_log_path)))

            self.melde(self.T("log_move_to_dupes_enabled"), "info")

            gruppen = self.gruppiere(alle)
            # Gruppen mit mehr als einer Datei sind Duplikat-Kandidaten.
            # Zusaetzlich wird eine einzelne Datei mit Nummer (_1, _2, ...)
            # umbenannt, wenn die Basisdatei fehlt.
            relevante = self._relevante_gruppen(gruppen)
            self.stat["gruppen"] = len(relevante)
            self.melde(self.T("log_dedup_groups", n=len(relevante)))

            self.log.put(("phase", "sort"))
            total_pruef = sum(len(v) for v in relevante.values())

            idx = 0
            for eintraege in relevante.values():
                if self.stop.is_set():
                    self.melde(self.T("log_cancelled"), "warn")
                    break

                eintraege.sort(key=lambda x: (x[1], x[0]))
                first_path, first_num = eintraege[0]

                keep_path = first_path
                if first_num > 0:
                    d = os.path.dirname(first_path)
                    orig_name = os.path.basename(first_path)
                    stem, ext = os.path.splitext(orig_name)
                    m = self.SUFFIX_RE.match(stem)
                    if m:
                        base_stem_orig = m.group("base")
                        base_path = os.path.join(d, base_stem_orig + ext)
                        if not os.path.exists(base_path):
                            try:
                                if not self.trockenlauf:
                                    os.rename(first_path, base_path)
                                    self.stat["umbenannt"] += 1
                                    self.melde(
                                        self.T("log_dedup_rename", old=first_path, new=base_path),
                                        "info",
                                    )
                                else:
                                    self.stat["umbenannt"] += 1
                                    self.melde(
                                        self.T(
                                            "log_dedup_rename_dry", old=first_path, new=base_path
                                        ),
                                        "info",
                                    )
                                keep_path = base_path
                            except Exception as e:
                                self.melde(self.T("log_error_generic", e=e), "error")
                                self.stat["fehler"] += 1
                                self.error_liste.append((first_path, str(e)))
                                keep_path = first_path

                hash_source = first_path if self.trockenlauf else keep_path
                keep_hash = hash_datei(hash_source)
                if keep_hash is None:
                    self.stat["fehler"] += 1
                    self.error_liste.append((hash_source, "unreadable"))
                    idx += 1
                    self.melde_progress(idx, total_pruef)
                    continue

                self.stat["behalten"] += 1
                self.melde(self.T("log_dedup_keep", path=keep_path), "info")

                for p, _num in eintraege[1:]:
                    if self.stop.is_set():
                        break
                    idx += 1
                    try:
                        if not os.path.exists(p):
                            continue

                        if self.force:
                            self._handle_duplicate(p, keep_path, force=True)
                            ordner = os.path.dirname(p)
                            self.pro_ordner[ordner] = self.pro_ordner.get(ordner, 0) + 1
                        else:
                            h = hash_datei(p)
                            if h is None:
                                self.stat["fehler"] += 1
                                self.error_liste.append((p, "unreadable"))
                                continue
                            if h == keep_hash:
                                self._handle_duplicate(p, keep_path, force=False)
                                ordner = os.path.dirname(p)
                                self.pro_ordner[ordner] = self.pro_ordner.get(ordner, 0) + 1
                            else:
                                self.stat["unterschiedlich"] += 1
                                self.melde(self.T("report_dedup_diff", path=p), "info")
                    except Exception as e:
                        self.stat["fehler"] += 1
                        self.error_liste.append((p, str(e)))
                        self.melde(self.T("log_error_generic", e=e), "error")

                    self._melde_fortschritt(idx, total_pruef)

            self._report()

        except Exception as e:
            self.melde(self.T("log_error_generic", e=e), "error")
        finally:
            if self._dry_log is not None:
                try:
                    self._dry_log.close()
                except Exception:
                    pass
                self._dry_log = None
            self.melde_finished()

    def _handle_duplicate(self, p, keep_path, force):
        dst = self._dupes_dst(p)
        if dst is None:
            self.stat["fehler"] += 1
            self.error_liste.append((p, "no source drive"))
            self.melde(self.T("log_error_generic", e="no source drive"), "error")
            return
        dst = self._unique_path(dst)
        if not self.trockenlauf:
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(p, dst)
                self.stat["verschoben"] += 1
                if force:
                    self.stat["force_geloescht"] += 1
                self.melde(self.T("log_dedup_move", src=p, dst=dst), "warn")
            except Exception as e:
                self.stat["fehler"] += 1
                self.error_liste.append((p, str(e)))
                self.melde(self.T("log_error_generic", e=e), "error")
                return
        else:
            self.stat["verschoben"] += 1
            if force:
                self.stat["force_geloescht"] += 1
            self.melde(self.T("log_dedup_move_dry", src=p, dst=dst), "warn")

        keeper_dst = self._dupes_dst(keep_path)
        if keeper_dst and keep_path not in self.copied_keepers:
            keeper_dst = self._unique_path(keeper_dst)
            if not self.trockenlauf:
                try:
                    if not os.path.exists(keeper_dst):
                        os.makedirs(os.path.dirname(keeper_dst), exist_ok=True)
                        shutil.copy2(keep_path, keeper_dst)
                        self.stat["keeper_kopiert"] += 1
                        self.melde(
                            self.T("log_dedup_copy_keeper", src=keep_path, dst=keeper_dst), "info"
                        )
                except Exception as e:
                    self.stat["fehler"] += 1
                    self.error_liste.append((keep_path, str(e)))
                    self.melde(self.T("log_error_generic", e=e), "error")
            else:
                self.stat["keeper_kopiert"] += 1
                self.melde(
                    self.T("log_dedup_copy_keeper_dry", src=keep_path, dst=keeper_dst), "info"
                )
            self.copied_keepers.add(keep_path)

    def _report(self):
        self.melde("")
        self.melde("=" * 60, "report")
        self.melde(self.T("report_title"), "report")
        self.melde("=" * 60, "report")
        self.melde(self.T("report_dedup_moved", n=self.stat["verschoben"]), "report")
        self.melde(self.T("report_dedup_keeper_copies", n=self.stat["keeper_kopiert"]), "report")
        self.melde(self.T("report_dedup_kept", n=self.stat["behalten"]), "report")
        _total = self.stat.get("gesamt", 0)
        _removed = self.stat["verschoben"]
        _remaining = _total - _removed
        if _remaining < 0:
            _remaining = 0
        self.melde(self.T("report_dedup_remaining", n=_remaining, total=_total), "report")
        self.melde(self.T("report_dedup_renamed", n=self.stat["umbenannt"]), "report")
        _copy = self.stat["behalten"]
        _dedup = self.stat["verschoben"]
        self.melde(self.T("report_dedup_summary", copy=_copy, dedup=_dedup), "report")
        if self.force:
            self.melde(
                self.T("report_dedup_forced_moved", n=self.stat["force_geloescht"]), "report"
            )
        self.melde(self.T("report_errors", n=self.stat["fehler"]), "report")

        if self.error_liste:
            self.melde("")
            self.melde(self.T("report_error_details"), "report")
            for p, msg in self.error_liste:
                self.melde(f"  {p}  ->  {msg}", "report")

        if self.pro_ordner:
            self.melde("")
            self.melde(self.T("report_dup_per_folder"), "report")
            for ordner, anzahl in sorted(self.pro_ordner.items(), key=lambda x: -x[1]):
                self.melde(f"  {anzahl:5d} x  {ordner}", "report")

        if self.trockenlauf and self._dry_log_path is not None:
            self.melde("", "report")
            self.melde(self.T("log_drylogfile", path=str(self._dry_log_path)), "report")

        self.melde(self.T("log_finished"), "report")
