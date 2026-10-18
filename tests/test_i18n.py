"""Tests fuer Konsistenz der Uebersetzungen und Hilfetexte."""

import ast
import re
from pathlib import Path

from help_texts import HELP_SECTIONS, get_help
from translations import TRANSLATIONS

PROJEKT = Path(__file__).resolve().parent.parent


def test_alle_sprachen_haben_gleiche_keys():
    base = set(TRANSLATIONS["de"].keys())
    for code, table in TRANSLATIONS.items():
        fehlend = base - set(table.keys())
        extra = set(table.keys()) - base
        assert not fehlend, f"Sprache {code}: fehlende Keys {sorted(fehlend)}"
        assert not extra, f"Sprache {code}: ueberzaehlige Keys {sorted(extra)}"


def test_help_sections_keys_existieren():
    for section, keys in HELP_SECTIONS.items():
        for code, table in TRANSLATIONS.items():
            for key in keys:
                assert key in table, f"{code}: Hilfe-Key '{key}' fehlt ({section})"


def test_get_help_liefert_text():
    for code in TRANSLATIONS:
        for section in HELP_SECTIONS:
            assert get_help(code, section).strip(), f"{code}/{section} leer"


def test_get_help_hat_keine_rohen_platzhalter():
    """Im Hilfetext darf kein rohes {nodate} stehen."""
    for code in TRANSLATIONS:
        for section in HELP_SECTIONS:
            assert "{nodate}" not in get_help(code, section), f"{code}/{section}"


def _quell_strings():
    """Alle String-Literale aus den Projekt-.py-Dateien (ohne Tests, .venv)."""
    gefunden = set()
    for pfad in PROJEKT.glob("*.py"):
        tree = ast.parse(pfad.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                gefunden.add(node.value)
    return gefunden


def test_keine_unbenutzten_keys():
    benutzt = _quell_strings()
    unbenutzt = sorted(k for k in TRANSLATIONS["de"] if k not in benutzt)
    assert not unbenutzt, f"Uebersetzt, aber nirgends verwendet: {unbenutzt}"


def test_translations_einheitlich_eingerueckt():
    """Sprachdateien: 4 Leerzeichen pro Ebene, keine Tabs."""
    dateien = [PROJEKT / "translations" / f"{code}.py" for code in TRANSLATIONS]
    for datei in dateien:
        assert datei.exists(), f"{datei} fehlt"
        quelle = datei.read_text(encoding="utf-8")
        for nr, zeile in enumerate(quelle.splitlines(), 1):
            einzug = len(zeile) - len(zeile.lstrip())
            assert "\t" not in zeile[:einzug], f"{datei.name}: Zeile {nr}: Tab statt Leerzeichen"
            if re.match(r'^\s*"[a-z0-9_]+":', zeile):
                assert einzug == 4, f"{datei.name}: Zeile {nr}: Schluessel mit {einzug} Einzug"


def test_sprachmodule_exportieren_dicts():
    """Jede Sprache liegt in einer eigenen Datei und exportiert ein Dict."""
    from importlib import import_module

    for code in TRANSLATIONS:
        modul = import_module(f"translations.{code}")
        assert isinstance(getattr(modul, code.upper()), dict), f"translations.{code}"
