"""Konfiguration und Konstanten fuer den Sortierer.

Gegliedert in: optionale Abhaengigkeiten, App-Verzeichnis, Dateitypen,
Ordnernamen und GUI-Optionen.
"""

import os

# ============================ Optionale Abhaengigkeiten =====================


def _lade_pillow():
    """Liest Pillow optional ein.

    Ohne (oder mit defektem) Pillow wird nur kein EXIF-Datum gelesen; die
    Sortierung laeuft dann ueber Video-Metadaten bzw. den Dateinamen weiter.
    Liefert (verfuegbar, Image-Modul).
    """
    try:
        from PIL import Image
    except Exception:
        return False, None
    try:
        # Sehr grosse Bilder sollen nur gewarnt, nicht blockiert werden.
        Image.MAX_IMAGE_PIXELS = 500_000_000
    except Exception:
        pass
    return True, Image


PIL_OK, Image = _lade_pillow()


# ============================ App-Verzeichnis ===============================

# Ablage fuer Logdatei (app.log) und Einstellungen (settings.json)
APP_DIR = os.path.join(os.path.expanduser("~"), ".medien_sortierer")


def app_dir():
    """Liefert das App-Verzeichnis und legt es bei Bedarf an.

    Laesst es sich nicht anlegen (z. B. wegen Rechten), wird das
    Benutzerverzeichnis zurueckgegeben, damit die App weiter startet.
    """
    try:
        os.makedirs(APP_DIR, exist_ok=True)
        return APP_DIR
    except Exception:
        return os.path.expanduser("~")


# ============================ Dateitypen ====================================

BILD_EXT = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".heic",
    ".webp",
    ".raw",
    ".cr2",
    ".nef",
    ".arw",
    ".orf",
    ".dng",
}

VIDEO_EXT = {
    ".mp4",
    ".m4v",
    ".m4p",
    ".mov",
    ".qt",
    ".avi",
    ".mkv",
    ".mk3d",
    ".wmv",
    ".asf",
    ".flv",
    ".f4v",
    ".f4p",
    ".f4a",
    ".f4b",
    ".mpg",
    ".mpeg",
    ".mpe",
    ".mp2",
    ".mpv",
    ".m1v",
    ".m2v",
    ".m2p",
    ".ps",
    ".ts",
    ".tsv",
    ".mts",
    ".m2ts",
    ".3gp",
    ".3g2",
    ".webm",
    ".ogv",
    ".ogx",
    ".ogg",
    ".drc",
    ".vob",
    ".evo",
    ".mxf",
    ".roq",
    ".nsv",
    ".divx",
    ".braw",
    ".yuv",
    ".rm",
    ".rmvb",
    ".viv",
    ".amv",
    ".svi",
    ".thp",
    ".smk",
    ".swf",
    ".gifv",
    ".mng",
}

# ============================ Ordner und Dateinamen =========================

# Eigene Steuer-/Logdateien, die nie als Medien gelten
SKIP_NAMES = {"_log.txt", "_log_dry.txt", "_liste.txt", "_index.txt"}

# Ordner fuer aussortierte Duplikate; wird vom Sorter uebersprungen
DUPES_FOLDER = "Duplicates"

# Frueherer Name des Ordners. Er wird weiterhin uebersprungen, damit Bestaende
# aus alten Laeufen nicht als normale Medien erneut einsortiert werden.
DUPES_FOLDER_ALTE = ("_Duplikate",)


def ist_dupes_ordner(name):
    """True, wenn *name* der Duplikat-Ordner ist (aktueller oder alter Name)."""
    return name == DUPES_FOLDER or name in DUPES_FOLDER_ALTE


# Unterordner, der angelegt wird, wenn Quelle und Ziel identisch sind
SORT_UNTERORDNER = "Sorted"

# Ordnernamen im Ziel: bewusst fest auf Englisch und NICHT uebersetzt, damit
# die Ordnerstruktur unabhaengig von der eingestellten Sprache gleich bleibt.
FOLDER_PICTURES = "Pictures"
FOLDER_VIDEOS = "Videos"
FOLDER_NO_DATE = "_No_Date"


# ============================ GUI-Optionen ==================================

WINDOW_TITLE = "Pictures and Video Sorter"

NAMING_OPTIONS = [
    ("original", "naming_original"),
    ("datum_name", "naming_datum_name"),
    ("datum_zeit_name", "naming_datum_zeit_name"),
    ("iso_name", "naming_iso_name"),
    ("nummer", "naming_nummer"),
    ("datum_nummer", "naming_datum_nummer"),
]

GRAN_OPTIONS = [
    ("year", "gran_year"),
    ("month", "gran_month"),
    ("day", "gran_day"),
]

STRUCT_OPTIONS = [
    ("separate", "rb_separate"),
    ("together", "rb_together"),
]
