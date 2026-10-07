"""Konfiguration und Konstanten fuer den Sortierer."""

try:
    from PIL import Image
    PIL_OK = True
    Image.MAX_IMAGE_PIXELS = 500_000_000
except ImportError:
    PIL_OK = False
    Image = None


BILD_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff",
            ".heic", ".webp", ".raw", ".cr2", ".nef", ".arw", ".orf", ".dng"}

VIDEO_EXT = {
    ".mp4", ".m4v", ".m4p", ".mov", ".qt", ".avi", ".mkv", ".mk3d",
    ".wmv", ".asf", ".flv", ".f4v", ".f4p", ".f4a", ".f4b",
    ".mpg", ".mpeg", ".mpe", ".mp2", ".mpv", ".m1v", ".m2v",
    ".m2p", ".ps", ".ts", ".tsv", ".mts", ".m2ts", ".3gp", ".3g2",
    ".webm", ".ogv", ".ogx", ".ogg", ".drc", ".vob", ".evo",
    ".mxf", ".roq", ".nsv", ".divx", ".braw", ".yuv", ".rm", ".rmvb",
    ".viv", ".amv", ".svi", ".thp", ".smk", ".swf", ".gifv", ".mng",
}

SKIP_NAMES = {"_log.txt", "_log_dry.txt", "_liste.txt", "_index.txt"}

WINDOW_TITLE = "Pictures and Video Sorter"

NAMING_OPTIONS = [
    ("original",        "naming_original"),
    ("datum_name",      "naming_datum_name"),
    ("datum_zeit_name", "naming_datum_zeit_name"),
    ("iso_name",        "naming_iso_name"),
    ("nummer",          "naming_nummer"),
    ("datum_nummer",    "naming_datum_nummer"),
]

GRAN_OPTIONS = [
    ("year",  "gran_year"),
    ("month", "gran_month"),
    ("day",   "gran_day"),
]

STRUCT_OPTIONS = [
    ("separate", "rb_separate"),
    ("together", "rb_together"),
]

# Unterordner, der angelegt wird, wenn Quelle und Ziel identisch sind
SORT_UNTERORDNER = "Sort"
