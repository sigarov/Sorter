"""Gemeinsame Basis fuer Sorter und DedupSorter.

Beide Worker teilen sich Quellen-/Filterverwaltung, Log-Ausgabe und das
Einsammeln der Mediendateien. Die eigentlichen Ablaeufe (Kopieren bzw.
Entdoppeln) stecken in den Unterklassen.
"""

import os
import threading

from config import BILD_EXT, SKIP_NAMES, VIDEO_EXT, ist_dupes_ordner


class MediaWorker(threading.Thread):
    """Basisklasse mit Quellen, Filtern, Log-Queue und Scan-Logik."""

    def __init__(self, quelle1, quelle2, ordner1, ordner2, lang, log_queue, stop_event):
        super().__init__(daemon=True)
        self.laufwerke = [
            (quelle1, [o.strip().lower() for o in ordner1 if o.strip()]),
            (quelle2, [o.strip().lower() for o in ordner2 if o.strip()]),
        ]
        self.lang = lang
        self.log = log_queue
        self.stop = stop_event
        self.error_liste = []

    # ---------- Uebersetzung und Ausgabe ----------
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

    def melde_finished(self):
        self.log.put(("finished", None))

    def melde_progress(self, current, total):
        self.log.put(("sort_progress", (current, total)))

    def melde_fortschritt(self, idx, total, key, **werte):
        """Meldet den Fortschritt gedrosselt (alle 10 Dateien und am Ende)."""
        if idx % 10 == 0 or idx == total:
            self.melde(self.T(key, i=idx, total=total, **werte), "progress")
            self.melde_progress(idx, total)

    # ---------- Dateien einsammeln ----------
    def _ist_zielordner(self, pfad):
        """True, wenn *pfad* der Zielordner ist (Basisklasse: nie)."""
        return False

    @staticmethod
    def _filter_passt(root, base, dirs, filter_ordner):
        """True, wenn dieser Ordner oder ein Unterordner zum Filter passt."""
        rel = os.path.relpath(root, base)
        teile = [] if rel == "." else rel.split(os.sep)
        if any(t.lower() in filter_ordner for t in teile):
            return True
        return any(d.lower() in filter_ordner for d in dirs)

    def sammle_dateien(self, mit_laufwerk=False):
        """Sammelt alle Medien-Dateien aus den Quellordnern.

        Mit ``mit_laufwerk`` werden (pfad, laufwerk)-Tupel geliefert, sonst
        reine Pfade. Der Duplikat-Ordner (``Duplicates``, auch der alte Name)
        und der Zielordner werden nie mitgelaufen.
        """
        alle = []
        for laufwerk, filter_ordner in self.laufwerke:
            if not laufwerk or not os.path.exists(laufwerk):
                continue
            base = os.path.abspath(laufwerk)
            for root, dirs, files in os.walk(base):
                dirs[:] = [
                    d
                    for d in dirs
                    if not ist_dupes_ordner(d) and not self._ist_zielordner(os.path.join(root, d))
                ]
                if self._ist_zielordner(root):
                    dirs[:] = []
                    continue
                if filter_ordner and not self._filter_passt(root, base, dirs, filter_ordner):
                    dirs[:] = []
                    continue
                for f in files:
                    if f in SKIP_NAMES:
                        continue
                    ext = os.path.splitext(f)[1].lower()
                    if ext in BILD_EXT or ext in VIDEO_EXT:
                        pfad = os.path.join(root, f)
                        alle.append((pfad, laufwerk) if mit_laufwerk else pfad)
        return alle
