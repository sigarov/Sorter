"""Hilfsfunktionen: Hashing, Datumserkennung und sichere Dateioperationen."""

import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from config import PIL_OK, VIDEO_EXT, Image

log = logging.getLogger(__name__)

# Blockgroesse beim Hashen (groessere Bloecke = weniger Systemaufrufe)
HASH_BLOCK = 4 * 1024 * 1024

# Ab dieser Pfadlaenge wird unter Windows der Langpfad-Prefix gesetzt.
# 240 laesst bewusst Luft bis zur 260er-Grenze: der Kopierer haengt
# voruebergehend ".tmp" (4 Zeichen) an denselben Ordner an.
MAX_PFAD_OHNE_PREFIX = 240

# Vorcompilierte Muster fuer die Datumserkennung aus Dateinamen
_RE_KOMPAKT = re.compile(r"((?:19|20)\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])")
_RE_GETRENNT = re.compile(r"((?:19|20)\d{2})[-_.](\d{1,2})[-_.](\d{1,2})")
_RE_JAHR = re.compile(r"\b((?:19|20)\d{2})\b")


def lang_pfad(pfad):
    """Pfad mit Windows-Langpfad-Prefix, falls er sehr lang ist.

    Nur ab ``MAX_PFAD_OHNE_PREFIX`` Zeichen wird der Prefix gesetzt, damit
    normale Pfade unveraendert bleiben. Kurze Pfade werden bewusst *nicht*
    absolut gemacht, damit sich die Funktion wie ``os.fspath`` verhaelt.
    Auf anderen Systemen passiert nichts.
    """
    p = os.fspath(pfad)
    if os.name != "nt":
        return p
    if p.startswith("\\\\?\\"):
        return p
    try:
        abs_p = os.path.abspath(p)
    except Exception:
        return p
    if len(abs_p) < MAX_PFAD_OHNE_PREFIX:
        return p
    if abs_p.startswith("\\\\"):
        return "\\\\?\\UNC\\" + abs_p[2:]
    return "\\\\?\\" + abs_p


class _NullWriter:
    """Ersatz fuer eine Logdatei, die nicht geoeffnet werden konnte."""

    def write(self, *a, **k):
        pass

    def flush(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def dry_log_pfad(basis_verzeichnis=None):
    """Pfad zur Trockenlauf-Logdatei.

    Wenn ``basis_verzeichnis`` angegeben ist, wird dort gespeichert,
    sonst im aktuellen Arbeitsverzeichnis."""
    if basis_verzeichnis:
        return Path(basis_verzeichnis) / "_log_dry.txt"
    return Path.cwd() / "_log_dry.txt"


def lesbare_groesse(anzahl_bytes):
    """Formatiert eine Byte-Zahl lesbar, z. B. ``1.23 GB`` oder ``4.5 MB``."""
    mb = anzahl_bytes / (1024.0 * 1024.0)
    if mb >= 1024:
        return "%.2f GB" % (mb / 1024.0)
    if mb >= 1:
        return "%.1f MB" % mb
    return "%.1f KB" % (anzahl_bytes / 1024.0)


def freier_platz(pfad):
    """Freier Speicherplatz in Bytes fuer das Laufwerk von *pfad*.

    Liefert None, wenn er sich nicht ermitteln laesst (z. B. Netzlaufwerk);
    Aufrufer behandeln None als "unbekannt, nicht abbrechen".
    """
    try:
        return shutil.disk_usage(lang_pfad(pfad)).free
    except Exception:
        log.debug("Freier Platz fuer %s nicht ermittelbar", pfad, exc_info=True)
        return None


def hash_datei(pfad, block=HASH_BLOCK):
    """MD5 ueber die komplette Datei.

    MD5 bleibt bewusst erhalten, damit bereits erzeugte ``_index.txt``-Dateien
    weiterhin gueltig sind. Liefert None, wenn die Datei nicht lesbar ist.
    """
    h = hashlib.md5()
    try:
        with open(lang_pfad(pfad), "rb") as f:
            while True:
                b = f.read(block)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()
    except Exception:
        log.debug("Hash fehlgeschlagen fuer %s", pfad, exc_info=True)
        return None


def kopiere_verifiziert(src, dst):
    """Kopiert *src* nach *dst* atomar und prueft die Dateigroesse.

    Es wird zuerst in eine ``.tmp``-Datei geschrieben und erst nach
    erfolgreicher Groessenpruefung umbenannt. Dadurch bleibt bei einem
    Abbruch keine halbe Datei im Ziel liegen. Bei Problemen wird eine
    Exception ausgeloest; die ``.tmp``-Datei wird dann entfernt.
    """
    ziel = Path(dst)
    tmp = ziel.with_name(ziel.name + ".tmp")
    try:
        shutil.copy2(lang_pfad(src), lang_pfad(tmp))
        groesse_src = os.path.getsize(lang_pfad(src))
        groesse_tmp = os.path.getsize(lang_pfad(tmp))
        if groesse_src != groesse_tmp:
            raise IOError(f"Groesse weicht ab: {groesse_src} != {groesse_tmp}")
        os.replace(lang_pfad(tmp), lang_pfad(ziel))
        return True
    except Exception:
        try:
            if os.path.exists(lang_pfad(tmp)):
                os.remove(lang_pfad(tmp))
        except Exception:
            log.debug("tmp-Datei nicht entfernbar: %s", tmp, exc_info=True)
        raise


def exif_datum(pfad):
    """EXIF-Aufnahmedatum oder None.

    Nutzt ``with``, damit das Bild auch bei Fehlern geschlossen wird.
    """
    if not PIL_OK:
        return None
    try:
        with Image.open(lang_pfad(pfad)) as img:
            exif = img.getexif()
            if not exif:
                return None
            for tag_id in (36867, 36868, 306):
                val = exif.get(tag_id)
                if not val:
                    continue
                try:
                    return datetime.strptime(str(val), "%Y:%m:%d %H:%M:%S")
                except ValueError:
                    pass
    except Exception:
        log.debug("EXIF nicht lesbar fuer %s", pfad, exc_info=True)
    return None


_FFPROBE_STATUS = None


def _ffprobe_vorhanden():
    """Prueft einmalig, ob ffprobe im PATH liegt."""
    global _FFPROBE_STATUS
    if _FFPROBE_STATUS is None:
        try:
            _FFPROBE_STATUS = shutil.which("ffprobe") is not None
        except Exception:
            _FFPROBE_STATUS = False
    return _FFPROBE_STATUS


def video_datum(pfad):
    """Aufnahmedatum aus Video-Metadaten (optional, ueber ffprobe).

    Ist ffprobe nicht installiert, wird None zurueckgegeben; die Sortierung
    laeuft dann ueber die weiteren Quellen weiter.
    """
    if not _ffprobe_vorhanden():
        return None
    kwargs = {}
    if os.name == "nt" and hasattr(subprocess, "CREATE_NO_WINDOW"):
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    try:
        ergebnis = subprocess.run(
            [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_entries",
                "format_tags=creation_time",
                lang_pfad(pfad),
            ],
            capture_output=True,
            text=True,
            timeout=20,
            **kwargs,
        )
        if ergebnis.returncode != 0:
            return None
        daten = json.loads(ergebnis.stdout or "{}")
    except Exception:
        log.debug("Video-Metadaten nicht lesbar fuer %s", pfad, exc_info=True)
        return None

    tags = (daten.get("format") or {}).get("tags") or {}
    wert = tags.get("creation_time") or tags.get("creationTime")
    if not wert:
        return None
    text = str(wert).strip()
    if text.endswith("Z"):
        text = text[:-1]
    text = text.split(".")[0]
    for muster in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text, muster)
        except ValueError:
            continue
    return None


def datum_aus_name(dateiname):
    """Datum aus dem Dateinamen ableiten.

    Reihenfolge: kompaktes Datum (20200102), getrenntes Datum (2020-01-02,
    2020.01.02, 2020_01_02), zuletzt nur das Jahr (dann 1. Januar).

    Hinweis: Ein reines Jahr direkt hinter einem Unterstrich (``DSC_2015``)
    wird nicht erkannt, weil ``_`` ein Wortzeichen ist und die Wortgrenze
    dort nicht greift. Dieses Verhalten ist durch Tests abgesichert.
    """
    name = dateiname
    for m in _RE_KOMPAKT.finditer(name):
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    for m in _RE_GETRENNT.finditer(name):
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    for m in _RE_JAHR.finditer(name):
        jahr = int(m.group(1))
        if 1970 <= jahr <= datetime.now().year:
            return datetime(jahr, 1, 1)
    return None


def ermittle_datum(pfad):
    """Ermittelt (Datum, Quelle) fuer eine Mediendatei.

    Reihenfolge: EXIF -> Video-Metadaten -> Dateiname. Ein Datum aus dem
    Dateisystem wird bewusst nicht verwendet, damit Dateien ohne echte
    Zeitangabe weiterhin im Ordner fuer Dateien ohne Datum landen.
    """
    datum = exif_datum(pfad)
    if datum:
        return datum, "EXIF"

    ext = os.path.splitext(os.fspath(pfad))[1].lower()
    if ext in VIDEO_EXT:
        datum = video_datum(pfad)
        if datum:
            return datum, "Video"

    datum = datum_aus_name(os.path.basename(os.fspath(pfad)))
    if datum:
        return datum, "Name"
    return None, "ohne"
