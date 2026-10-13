"""Stellt sicher, dass gui.py nur existierende Uebersetzungs-Keys nutzt."""

import re
from pathlib import Path

from translations import TRANSLATIONS

GUI_PFAD = Path(__file__).resolve().parent.parent / "gui.py"

# Literale Zugriffe wie L["key"], L.get("key", ...),
# self.lang["key"] und self.lang.get("key", ...).
_MUSTER = [
    r'L\.get\(\s*"([a-z_]+)"\s*[,)]',
    r'L\[\s*"([a-z_]+)"\s*\]',
    r'self\.lang\.get\(\s*"([a-z_]+)"\s*[,)]',
    r'self\.lang\[\s*"([a-z_]+)"\s*\]',
]


def _verwendete_keys():
    src = GUI_PFAD.read_text(encoding="utf-8")
    keys = set()
    for muster in _MUSTER:
        keys.update(re.findall(muster, src))
    return keys


def test_gui_verwendet_nur_vorhandene_keys():
    vorhanden = set(TRANSLATIONS["de"].keys())
    fehlend = sorted(_verwendete_keys() - vorhanden)
    assert not fehlend, f"In gui.py verwendet, aber nicht uebersetzt: {fehlend}"
