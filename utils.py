"""Hilfsfunktionen: Hashing, EXIF- und Namensdatum."""

import hashlib
import re
from datetime import datetime
from pathlib import Path

from config import PIL_OK, Image


class _NullWriter:
    def write(self, *a, **k): pass
    def flush(self): pass
    def close(self): pass
    def __enter__(self): return self
    def __exit__(self, *a): return False

def dry_log_pfad(basis_verzeichnis=None):
    """Liefert den Pfad zur Trockenlauf-Logdatei.
    Wenn basis_verzeichnis angegeben ist, wird dort gespeichert,
    sonst im aktuellen Arbeitsverzeichnis."""
    if basis_verzeichnis:
        return Path(basis_verzeichnis) / "_log_dry.txt"
    return Path.cwd() / "_log_dry.txt"

def hash_datei(pfad, block=1024 * 1024):
    h = hashlib.md5()
    try:
        with open(pfad, "rb") as f:
            while True:
                b = f.read(block)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()
    except Exception:
        return None

def exif_datum(pfad):
    if not PIL_OK:
        return None
    try:
        img = Image.open(pfad)
        exif = img.getexif()
        if not exif:
            return None
        for tag_id in (36867, 306):
            val = exif.get(tag_id)
            if val:
                try:
                    return datetime.strptime(str(val), "%Y:%m:%d %H:%M:%S")
                except ValueError:
                    pass
    except Exception:
        pass
    return None

def datum_aus_name(dateiname):
    name = dateiname
    for m in re.finditer(r"((?:19|20)\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])", name):
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    for m in re.finditer(r"((?:19|20)\d{2})[-_.](\d{1,2})[-_.](\d{1,2})", name):
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    for m in re.finditer(r"\b((?:19|20)\d{2})\b", name):
        jahr = int(m.group(1))
        if 1970 <= jahr <= datetime.now().year:
            return datetime(jahr, 1, 1)
    return None
