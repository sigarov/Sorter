"""Sorter-Thread: kopiert und sortiert Medien in den Zielordner."""

import os
import re
import shutil
import threading
from datetime import datetime
from pathlib import Path

from config import BILD_EXT, VIDEO_EXT, SKIP_NAMES, NAMING_OPTIONS
from utils import _NullWriter, dry_log_pfad, hash_datei, exif_datum, datum_aus_name


class Sorter(threading.Thread):
    def __init__(self, quelle1, quelle2, ordner1, ordner2, ziel,
                 trockenlauf, skip_existing, gemeinsam, granularitaet, naming,
                 lang, log_queue, stop_event, ziel_umgeleitet=False):
        super().__init__(daemon=True)
        self.laufwerke = [
            (quelle1, [o.strip().lower() for o in ordner1 if o.strip()]),
            (quelle2, [o.strip().lower() for o in ordner2 if o.strip()]),
        ]
        self.ziel = Path(ziel)
        self.ziel_umgeleitet = ziel_umgeleitet
        self._ziel_norm = os.path.normcase(os.path.abspath(str(self.ziel)))
        self.trockenlauf = trockenlauf
        self.skip_existing = skip_existing
        self.gemeinsam = gemeinsam
        self.granularitaet = granularitaet
        self.naming = naming
        self.lang = lang
        self.log = log_queue
        self.stop = stop_event
        self.stat = {"neu": 0, "dup": 0, "fehler": 0, "gesamt": 0, "ohne_datum": 0}
        self.dup_pro_ordner = {}
        self.ohne_datum_liste = []
        self.nummer_counter = {}
        self.index_entries = {}
        self.no_date_folder = lang.get("folder_no_date", "_Ohne_Datum")
        self.folder_pictures = lang.get("folder_pictures", "Bilder")
        self.folder_videos = lang.get("folder_videos", "Videos")
        self._dry_log_path = None
        self.error_liste = []

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

    def melde_index(self, current, total):
        self.log.put(("index", (current, total)))

    def melde_sort_progress(self, current, total):
        self.log.put(("sort_progress", (current, total)))

    def melde_finished(self):
        self.log.put(("finished", None))

    def sammle_dateien(self):
        alle = []
        for laufwerk, filter_ordner in self.laufwerke:
            if not laufwerk or not os.path.exists(laufwerk):
                continue
            base = os.path.abspath(laufwerk)
            for root, dirs, files in os.walk(base):
                # Zielordner nie mit-scannen (verhindert Re-Sortieren)
                if os.path.normcase(os.path.abspath(root)) == self._ziel_norm:
                    dirs[:] = []
                    continue
                dirs[:] = [d for d in dirs
                           if os.path.normcase(os.path.abspath(
                               os.path.join(root, d))) != self._ziel_norm]
                if filter_ordner:
                    rel = os.path.relpath(root, base)
                    teile = [] if rel == "." else rel.split(os.sep)
                    drin = any(t.lower() in filter_ordner for t in teile)
                    if not drin:
                        if not any(d.lower() in filter_ordner for d in dirs):
                            dirs[:] = []
                            continue
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in BILD_EXT or ext in VIDEO_EXT:
                        alle.append((os.path.join(root, f), laufwerk))
        return alle

    def lade_index(self):
        idx = {}
        index_file = self.ziel / "_index.txt"
        if not index_file.exists():
            return idx
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip("\n")
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split("|", 3)
                    if len(parts) != 4:
                        continue
                    h, size_s, mtime_s, rel = parts
                    idx[rel] = (h, size_s, mtime_s)
        except Exception as e:
            self.melde(self.T("log_index_read_error", e=e), "warn")
        return idx

    def speichere_index(self):
        index_file = self.ziel / "_index.txt"
        try:
            tmp = self.ziel / "_index.txt.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(f"# MedienSortierer Index - {datetime.now()}\n")
                f.write(f"# Format: md5_hash|size|mtime_ns|relativer_pfad\n")
                for rel, (h, size_s, mtime_s) in self.index_entries.items():
                    f.write(f"{h}|{size_s}|{mtime_s}|{rel}\n")
            tmp.replace(index_file)
        except Exception as e:
            self.melde(self.T("log_index_save_error", e=e), "warn")

    def indexiere_ziel(self):
        known = {}
        self.index_entries = {}

        if self.trockenlauf and not self.ziel.exists():
            self.melde(self.T("log_found_target", n=0))
            self.melde_index(0, 0)
            self.melde(self.T("log_index_loaded", n=0))
            return known

        self.melde(self.T("log_counting_target"))
        alle_ziel = []
        for root, _, files in os.walk(self.ziel):
            for f in files:
                if f in SKIP_NAMES:
                    continue
                alle_ziel.append(os.path.join(root, f))
        total = len(alle_ziel)
        self.melde(self.T("log_found_target", n=total))
        self.melde_index(0, total)

        cached = self.lade_index()
        self.melde(self.T("log_index_loaded", n=len(cached)))

        neu_berechnet = 0
        cache_hits = 0
        fehlend = 0

        for i, p in enumerate(alle_ziel, 1):
            if self.stop.is_set():
                self.melde(self.T("log_index_broken"), "warn")
                break
            try:
                rel = os.path.relpath(p, self.ziel).replace("\\", "/")
                st = os.stat(p)
                size_s = str(st.st_size)
                mtime_s = str(st.st_mtime_ns)

                if rel in cached:
                    h_c, sz_c, mt_c = cached[rel]
                    if sz_c == size_s and mt_c == mtime_s:
                        known[h_c] = p
                        self.index_entries[rel] = (h_c, size_s, mtime_s)
                        cache_hits += 1
                    else:
                        h = hash_datei(p)
                        if h:
                            known[h] = p
                            self.index_entries[rel] = (h, size_s, mtime_s)
                            neu_berechnet += 1
                else:
                    h = hash_datei(p)
                    if h:
                        known[h] = p
                        self.index_entries[rel] = (h, size_s, mtime_s)
                        neu_berechnet += 1
            except Exception:
                fehlend += 1

            if i % 25 == 0 or i == total:
                self.melde_index(i, total)

        self.melde(self.T("log_index_done",
                          cache=cache_hits, new=neu_berechnet, skip=fehlend),
                   "info")
        return known

    def naechste_nummer(self, ziel_dir):
        key = str(ziel_dir)
        if key not in self.nummer_counter:
            max_n = 0
            if ziel_dir.exists():
                for f in ziel_dir.iterdir():
                    if f.is_file():
                        m = re.match(r"^(\d+)", f.stem)
                        if m:
                            try:
                                max_n = max(max_n, int(m.group(1)))
                            except ValueError:
                                pass
            self.nummer_counter[key] = max_n
        self.nummer_counter[key] += 1
        return self.nummer_counter[key]

    def neuer_dateiname(self, original_name, datum, ziel_dir):
        base = os.path.splitext(original_name)[0]
        ext = os.path.splitext(original_name)[1].lower()
        if datum is None:
            if self.naming == "nummer":
                n = self.naechste_nummer(ziel_dir)
                return f"{n:05d}{ext}"
            return f"{base}{ext}"
        if self.naming == "original":
            return f"{base}{ext}"
        elif self.naming == "datum_name":
            return f"{datum.strftime('%Y%m%d')}_{base}{ext}"
        elif self.naming == "datum_zeit_name":
            return f"{datum.strftime('%Y%m%d_%H%M%S')}_{base}{ext}"
        elif self.naming == "iso_name":
            return f"{datum.strftime('%Y-%m-%d')}_{base}{ext}"
        elif self.naming == "nummer":
            n = self.naechste_nummer(ziel_dir)
            return f"{n:05d}{ext}"
        elif self.naming == "datum_nummer":
            n = self.naechste_nummer(ziel_dir)
            return f"{datum.strftime('%Y%m%d')}_{n:04d}{ext}"
        return f"{base}{ext}"

    def datum_pfad_teile(self, datum):
        if self.granularitaet == "year":
            return [str(datum.year)]
        elif self.granularitaet == "month":
            return [str(datum.year), f"{datum.month:02d}"]
        else:
            return [str(datum.year), f"{datum.month:02d}", f"{datum.day:02d}"]

    def run(self):
        try:
            self.ziel.mkdir(parents=True, exist_ok=True)
            logdatei = self.ziel / "_log.txt"

            if self.trockenlauf:
                self.melde(self.T("log_dryrun_mode"), "warn")

            if self.ziel_umgeleitet:
                self.melde(self.T("log_ziel_gleich_quelle",
                                  path=str(self.ziel)), "warn")

            self.melde(self.T("log_collecting"))
            alle = self.sammle_dateien()
            self.stat["gesamt"] = len(alle)
            self.melde(self.T("log_found_sources", n=len(alle)))

            naming_label_key = None
            for key, tr_key in NAMING_OPTIONS:
                if key == self.naming:
                    naming_label_key = tr_key
                    break
            naming_name = self.lang.get(naming_label_key, self.naming) if naming_label_key else self.naming
            self.melde(self.T("log_naming_option", name=naming_name))

            self.log.put(("phase", "index"))
            self.melde(self.T("log_building_index"))
            known = self.indexiere_ziel()

            self.log.put(("phase", "sort"))

            # ---------- Logdatei öffnen ----------
            if self.trockenlauf:
                basis = None
                for lw, _ in self.laufwerke:
                    if lw and os.path.exists(lw):
                        basis = lw
                        break
                dry_path = dry_log_pfad(basis) if basis else dry_log_pfad()
                try:
                    lf_ctx = open(dry_path, "w", encoding="utf-8")
                    self._dry_log_path = dry_path
                    self.melde(self.T("log_drylogfile", path=str(dry_path)))
                except Exception as e:
                    self.melde(self.T("log_error_generic", e=e), "warn")
                    lf_ctx = _NullWriter()
            else:
                lf_ctx = open(logdatei, "a", encoding="utf-8")

            with lf_ctx as lf:
                lf.write(f"\n=== Start {datetime.now()} ===\n")
                if self.trockenlauf:
                    lf.write(f"*** DRY RUN – keine Dateien werden kopiert/verschoben ***\n")

                for i, (pfad, laufwerk) in enumerate(alle, 1):
                    if self.stop.is_set():
                        self.melde(self.T("log_cancelled"), "warn")
                        break
                    ext = os.path.splitext(pfad)[1].lower()
                    try:
                        h = hash_datei(pfad)
                        if h is None:
                            self.stat["fehler"] += 1
                            self.error_liste.append((pfad, "unreadable"))
                            lf.write(f"ERROR (read): {pfad}\n")
                            continue

                        if h in known:
                            self.stat["dup"] += 1
                            vorhandener = known[h]
                            zo = os.path.dirname(vorhandener)
                            self.dup_pro_ordner[zo] = \
                                self.dup_pro_ordner.get(zo, 0) + 1
                            lf.write(f"DUP: {pfad}\n     == {vorhandener}\n")
                            if i % 10 == 0 or i == len(alle):
                                self.melde(
                                    f"[{i}/{len(alle)}]  neu={self.stat['neu']}  "
                                    f"dup={self.stat['dup']}  "
                                    f"ohne_datum={self.stat['ohne_datum']}  "
                                    f"fehler={self.stat['fehler']}",
                                    "progress")
                                self.melde_sort_progress(i, len(alle))
                            continue

                        datum = exif_datum(pfad)
                        quelle_datum = "EXIF"
                        if not datum:
                            datum = datum_aus_name(os.path.basename(pfad))
                            quelle_datum = "Name" if datum else "ohne"

                        typ = self.folder_pictures if ext in BILD_EXT else self.folder_videos

                        if datum:
                            teile = self.datum_pfad_teile(datum)
                            if self.gemeinsam:
                                ziel_dir = self.ziel.joinpath(*teile)
                                unterordner_info = "/".join(teile)
                            else:
                                ziel_dir = self.ziel / typ
                                ziel_dir = ziel_dir.joinpath(*teile)
                                unterordner_info = "\\".join([typ] + teile)
                        else:
                            if self.gemeinsam:
                                ziel_dir = self.ziel / self.no_date_folder
                                unterordner_info = self.no_date_folder
                            else:
                                ziel_dir = self.ziel / self.no_date_folder / typ
                                unterordner_info = f"{self.no_date_folder}\\{typ}"
                            self.stat["ohne_datum"] += 1
                            self.ohne_datum_liste.append(pfad)

                        if not self.trockenlauf:
                            ziel_dir.mkdir(parents=True, exist_ok=True)

                        neuer_name = self.neuer_dateiname(
                            os.path.basename(pfad), datum, ziel_dir)
                        neu = ziel_dir / neuer_name

                        if neu.exists() and self.skip_existing:
                            self.stat["dup"] += 1
                            lf.write(f"SKIP (exists): {pfad} -> {neu}\n")
                            if i % 10 == 0 or i == len(alle):
                                self.melde(
                                    f"[{i}/{len(alle)}]  neu={self.stat['neu']}  "
                                    f"dup={self.stat['dup']}  "
                                    f"ohne_datum={self.stat['ohne_datum']}  "
                                    f"fehler={self.stat['fehler']}",
                                    "progress")
                                self.melde_sort_progress(i, len(alle))
                            continue

                        n = 1
                        stem = neu.stem
                        suf = neu.suffix
                        if not self.trockenlauf:
                            while neu.exists():
                                neu = ziel_dir / f"{stem}_{n}{suf}"
                                n += 1

                        if self.trockenlauf:
                            aktion = "DRY-COPY"
                        else:
                            shutil.copy2(pfad, str(neu))
                            aktion = "COPY"

                        if not self.trockenlauf:
                            known[h] = str(neu)
                            try:
                                st = os.stat(neu)
                                rel = os.path.relpath(str(neu), self.ziel).replace("\\", "/")
                                self.index_entries[rel] = (
                                    h, str(st.st_size), str(st.st_mtime_ns))
                            except Exception:
                                pass
                        else:
                            known[h] = str(neu)

                        self.stat["neu"] += 1
                        lf.write(f"{aktion} [{quelle_datum}] -> {unterordner_info}: "
                                 f"{pfad} -> {neu}\n")

                    except Exception as e:
                        self.stat["fehler"] += 1
                        self.error_liste.append((pfad, str(e)))
                        lf.write(f"ERROR: {pfad} - {e}\n")

                    if i % 10 == 0 or i == len(alle):
                        self.melde(
                            f"[{i}/{len(alle)}]  neu={self.stat['neu']}  "
                            f"dup={self.stat['dup']}  "
                            f"ohne_datum={self.stat['ohne_datum']}  "
                            f"fehler={self.stat['fehler']}",
                            "progress")
                        self.melde_sort_progress(i, len(alle))

                lf.write(f"=== Fertig {datetime.now()} ===\n")

                # ---- Report in die Logdatei schreiben ----
                lf.write("\n--- Report ---\n")
                lf.write(f"Neu: {self.stat['neu']} | Dup: {self.stat['dup']} | "
                         f"Ohne Datum: {self.stat['ohne_datum']} | "
                         f"Fehler: {self.stat['fehler']}\n")
                if self.dup_pro_ordner:
                    lf.write("Duplikate pro Ordner:\n")
                    for ordner, anzahl in sorted(self.dup_pro_ordner.items(),
                                                 key=lambda x: -x[1]):
                        lf.write(f"  {anzahl} x {ordner}\n")

            if not self.trockenlauf:
                self.melde(self.T("log_saving_index"))
                self.speichere_index()
                self.melde(self.T("log_index_saved", n=len(self.index_entries)))

                if self.ohne_datum_liste:
                    liste_pfad = self.ziel / self.no_date_folder / "_liste.txt"
                    liste_pfad.parent.mkdir(parents=True, exist_ok=True)
                    with open(liste_pfad, "w", encoding="utf-8") as f:
                        f.write(f"({len(self.ohne_datum_liste)}):\n")
                        f.write("=" * 60 + "\n")
                        for p in self.ohne_datum_liste:
                            f.write(p + "\n")

            self.melde("")
            self.melde("=" * 60, "report")
            self.melde(self.T("report_title"), "report")
            self.melde("=" * 60, "report")
            self.melde(self.T("report_new", n=self.stat['neu']), "report")
            self.melde(self.T("report_dup", n=self.stat['dup']), "report")
            self.melde(self.T("report_no_date",
                              n=self.stat['ohne_datum'],
                              path=str(self.ziel / self.no_date_folder)), "report")
            self.melde(self.T("report_errors", n=self.stat['fehler']), "report")

            if self.error_liste:
                self.melde("")
                self.melde(self.T("report_error_details"), "report")
                for p, msg in self.error_liste:
                    self.melde(f"  {p}  ->  {msg}", "report")

            if self.dup_pro_ordner:
                self.melde("")
                self.melde(self.T("report_dup_per_folder"), "report")
                for ordner, anzahl in sorted(self.dup_pro_ordner.items(),
                                             key=lambda x: -x[1]):
                    self.melde(f"  {anzahl:5d} x  {ordner}", "report")
            else:
                self.melde(self.T("report_no_dups"), "report")

            if not self.trockenlauf:
                self.melde("", "report")
                self.melde(self.T("log_logfile", path=str(logdatei)), "report")
            else:
                if self._dry_log_path is not None:
                    self.melde("", "report")
                    self.melde(self.T("log_drylogfile",
                                      path=str(self._dry_log_path)), "report")

            self.melde(self.T("log_finished"), "report")

        except Exception as e:
            self.melde(self.T("log_error_generic", e=e), "error")
        finally:
            self.melde_finished()
