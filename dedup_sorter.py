"""DedupSorter-Thread: entfernt/verschiebt _1, _2-Duplikate in den Quellordnern."""

import os
import re
import shutil
import threading
from datetime import datetime
from pathlib import Path

from config import BILD_EXT, VIDEO_EXT, SKIP_NAMES
from utils import _NullWriter, dry_log_pfad, hash_datei


class DedupSorter(threading.Thread):
    """Entfernt NAME_1.jpg, NAME_2.jpg, ... in den Quellordnern.

       Standard (force=False): nur behandeln, wenn byte-identisch zu NAME.jpg.
       force=True          : ALLE _1, _2, ... behandeln, egal ob der Inhalt
                             abweicht.
       Fehlt NAME.jpg, wird NAME_1.jpg in NAME.jpg umbenannt.
       move_to_dupes=True  : Duplikate werden nach <Quelle>/_Duplikate/<rel>
                             verschoben (statt geloescht). Der Keeper wird
                             einmal pro Gruppe mit hineinkopiert."""

    SUFFIX_RE = re.compile(r"^(?P<base>.+)_(?P<num>\d{1,2})$")
    DUPES_FOLDER = "_Duplikate"

    def __init__(self, quelle1, quelle2, ordner1, ordner2,
                 trockenlauf, force, move_to_dupes,
                 lang, log_queue, stop_event):
        super().__init__(daemon=True)
        self.laufwerke = [
            (quelle1, [o.strip().lower() for o in ordner1 if o.strip()]),
            (quelle2, [o.strip().lower() for o in ordner2 if o.strip()]),
        ]
        self.trockenlauf = trockenlauf
        self.force = force
        self.move_to_dupes = move_to_dupes
        self.lang = lang
        self.log = log_queue
        self.stop = stop_event
        self.stat = {"geloescht": 0, "verschoben": 0, "keeper_kopiert": 0,
                     "behalten": 0, "unterschiedlich": 0,
                     "fehler": 0, "gruppen": 0, "frei_bytes": 0,
                     "umbenannt": 0, "force_geloescht": 0,
                     "gesamt": 0}
        self.behalten_liste = []
        self.geloescht_liste = []
        self.diff_liste = []
        self.pro_ordner = {}
        self._dry_log = None
        self._dry_log_path = None
        self.error_liste = []
        self.copied_keepers = set()

    def T(self, key, **kw):
        s = self.lang.get(key, key)
        if kw:
            try:
                return s.format(**kw)
            except Exception:
                return s
        return s

    def melde(self, text, tag="info"):
        self.log.put((tag, text))
        if self._dry_log is not None:
            try:
                self._dry_log.write(f"{text}\n")
                self._dry_log.flush()
            except Exception:
                pass

    def melde_finished(self):
        self.log.put(("finished", None))

    def melde_dedup_progress(self, cur, tot):
        self.log.put(("sort_progress", (cur, tot)))

    def sammle_dateien(self):
        alle = []
        for laufwerk, filter_ordner in self.laufwerke:
            if not laufwerk or not os.path.exists(laufwerk):
                continue
            base = os.path.abspath(laufwerk)
            for root, dirs, files in os.walk(base):
                # _Duplikate-Ordner selbst ueberspringen
                dirs[:] = [d for d in dirs if d != self.DUPES_FOLDER]
                if filter_ordner:
                    rel = os.path.relpath(root, base)
                    teile = [] if rel == "." else rel.split(os.sep)
                    drin = any(t.lower() in filter_ordner for t in teile)
                    if not drin:
                        if not any(d.lower() in filter_ordner for d in dirs):
                            dirs[:] = []
                            continue
                for f in files:
                    if f in SKIP_NAMES:
                        continue
                    ext = os.path.splitext(f)[1].lower()
                    if ext in BILD_EXT or ext in VIDEO_EXT:
                        alle.append(os.path.join(root, f))
        return alle

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

    def _quelle_fuer_pfad(self, pfad):
        """Ermittelt das laengste passende Quelllaufwerk zum Pfad."""
        pfad_abs = os.path.abspath(pfad).lower()
        best = None
        best_len = -1
        for lw, _ in self.laufwerke:
            if not lw:
                continue
            lw_abs = os.path.abspath(lw).lower()
            if pfad_abs.startswith(lw_abs) and len(lw_abs) > best_len:
                best = lw
                best_len = len(lw_abs)
        return best

    def _dupes_dst(self, src_path):
        """Zielpfad <Quelle>/_Duplikate/<relativer Pfad>."""
        quelle = self._quelle_fuer_pfad(src_path)
        if not quelle:
            return None
        base = os.path.abspath(quelle)
        rel = os.path.relpath(src_path, base)
        return os.path.join(base, self.DUPES_FOLDER, rel)

    @staticmethod
    def _unique_path(path):
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        n = 1
        while os.path.exists(f"{base}_{n}{ext}"):
            n += 1
        return f"{base}_{n}{ext}"

    def run(self):
        try:
            if self.trockenlauf:
                basis = None
                for lw, _ in self.laufwerke:
                    if lw and os.path.exists(lw):
                        basis = lw
                        break
                dry_path = dry_log_pfad(basis) if basis else dry_log_pfad()
                try:
                    self._dry_log = open(dry_path, "w", encoding="utf-8")
                    self._dry_log_path = dry_path
                    self._dry_log.write(
                        f"=== DRY RUN (Dedup) {datetime.now()} ===\n")
                except Exception:
                    self._dry_log = None

            self.melde(self.T("log_dedup_start"))
            alle = self.sammle_dateien()
            self.stat["gesamt"] = len(alle)
            self.melde(self.T("log_found_sources", n=len(alle)))

            if self.trockenlauf:
                self.melde(self.T("log_dryrun_mode"), "warn")
                if self._dry_log_path is not None:
                    self.melde(self.T("log_drylogfile",
                                      path=str(self._dry_log_path)))

            if self.move_to_dupes:
                self.melde(self.T("log_move_to_dupes_enabled"), "info")

            gruppen = self.gruppiere(alle)
            relevante = {k: v for k, v in gruppen.items() if len(v) > 1}
            self.stat["gruppen"] = len(relevante)
            self.melde(self.T("log_dedup_groups", n=len(relevante)))

            self.log.put(("phase", "sort"))
            total_pruef = sum(len(v) for v in relevante.values())

            idx = 0
            for key, eintraege in relevante.items():
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
                                    self.melde(self.T("log_dedup_rename",
                                                      old=first_path,
                                                      new=base_path), "info")
                                else:
                                    self.stat["umbenannt"] += 1
                                    self.melde(self.T("log_dedup_rename_dry",
                                                      old=first_path,
                                                      new=base_path), "info")
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
                    self.melde_dedup_progress(idx, total_pruef)
                    continue

                self.stat["behalten"] += 1
                self.behalten_liste.append(keep_path)
                self.melde(self.T("log_dedup_keep", path=keep_path), "info")

                for p, num in eintraege[1:]:
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
                                self.diff_liste.append(p)
                                self.melde(self.T("report_dedup_diff", path=p), "info")
                    except Exception as e:
                        self.stat["fehler"] += 1
                        self.error_liste.append((p, str(e)))
                        self.melde(self.T("log_error_generic", e=e), "error")

                    if idx % 10 == 0 or idx == total_pruef:
                        self.melde(
                            f"[{idx}/{total_pruef}]  gelöscht={self.stat['geloescht']}  "
                            f"verschoben={self.stat['verschoben']}  "
                            f"behalten={self.stat['behalten']}  "
                            f"umbenannt={self.stat['umbenannt']}  "
                            f"verschieden={self.stat['unterschiedlich']}",
                            "progress")
                        self.melde_dedup_progress(idx, total_pruef)

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
        if self.move_to_dupes:
            dst = self._dupes_dst(p)
            if dst is None:
                self._do_delete(p, force=force)
                return
            dst = self._unique_path(dst)
            if not self.trockenlauf:
                try:
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.move(p, dst)
                    self.stat["verschoben"] += 1
                    self.geloescht_liste.append(p)
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
                self.geloescht_liste.append(p)
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
                            self.melde(self.T("log_dedup_copy_keeper",
                                              src=keep_path,
                                              dst=keeper_dst), "info")
                    except Exception as e:
                        self.stat["fehler"] += 1
                        self.error_liste.append((keep_path, str(e)))
                        self.melde(self.T("log_error_generic", e=e), "error")
                else:
                    self.stat["keeper_kopiert"] += 1
                    self.melde(self.T("log_dedup_copy_keeper_dry",
                                      src=keep_path,
                                      dst=keeper_dst), "info")
                self.copied_keepers.add(keep_path)
        else:
            self._do_delete(p, force=force)

    def _do_delete(self, p, force):
        if not self.trockenlauf:
            size = os.path.getsize(p)
            os.remove(p)
            self.stat["frei_bytes"] += size
            self.stat["geloescht"] += 1
            if force:
                self.stat["force_geloescht"] += 1
            self.geloescht_liste.append(p)
            self.melde(self.T("log_dedup_delete", path=p), "warn")
        else:
            self.stat["geloescht"] += 1
            if force:
                self.stat["force_geloescht"] += 1
            self.geloescht_liste.append(p)
            self.melde(self.T("log_dedup_dryrun", path=p), "warn")

    def _report(self):
        self.melde("")
        self.melde("=" * 60, "report")
        self.melde(self.T("report_title"), "report")
        self.melde("=" * 60, "report")
        self.melde(self.T("report_dedup_deleted", n=self.stat["geloescht"]), "report")
        if self.move_to_dupes:
            self.melde(self.T("report_dedup_moved",
                              n=self.stat["verschoben"]), "report")
            self.melde(self.T("report_dedup_keeper_copies",
                              n=self.stat["keeper_kopiert"]), "report")
        self.melde(self.T("report_dedup_kept",    n=self.stat["behalten"]), "report")
        _total     = self.stat.get("gesamt", 0)
        _removed   = self.stat["verschoben"] + self.stat["geloescht"]
        _remaining = _total - _removed
        if _remaining < 0:
            _remaining = 0
        self.melde(self.T("report_dedup_remaining",
                          n=_remaining, total=_total), "report")
        self.melde(self.T("report_dedup_renamed", n=self.stat["umbenannt"]), "report")
        _copy  = self.stat["behalten"]
        _dedup = self.stat["verschoben"] + self.stat["geloescht"]
        self.melde(self.T("report_dedup_summary",
                          copy=_copy, dedup=_dedup), "report")
        if self.force:
            if self.move_to_dupes:
                self.melde(self.T("report_dedup_forced_moved",
                                  n=self.stat["force_geloescht"]), "report")
            else:
                self.melde(self.T("report_dedup_forced",
                                  n=self.stat["force_geloescht"]), "report")
        self.melde(self.T("report_dedup_space",
                          mb=self.stat["frei_bytes"] / (1024 * 1024)), "report")
        self.melde(self.T("report_errors", n=self.stat["fehler"]), "report")

        if self.error_liste:
            self.melde("")
            self.melde(self.T("report_error_details"), "report")
            for p, msg in self.error_liste:
                self.melde(f"  {p}  ->  {msg}", "report")

        if self.pro_ordner:
            self.melde("")
            self.melde(self.T("report_dup_per_folder"), "report")
            for ordner, anzahl in sorted(self.pro_ordner.items(),
                                         key=lambda x: -x[1]):
                self.melde(f"  {anzahl:5d} x  {ordner}", "report")

        if self.trockenlauf and self._dry_log_path is not None:
            self.melde("", "report")
            self.melde(self.T("log_drylogfile",
                              path=str(self._dry_log_path)), "report")

        self.melde(self.T("log_finished"), "report")
