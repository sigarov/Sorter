"""Gemeinsame Testvorbereitung: Module importierbar, keine modalen Dialoge."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ohne tkinter (z. B. schlankes Linux ohne python3-tk) sind die GUI-Tests
# nicht lauffaehig. Nur dann werden sie gezielt ausgenommen, damit die
# uebrigen Tests trotzdem laufen.
try:
    import tkinter  # noqa: F401
except Exception:  # pragma: no cover - haengt von der Umgebung ab
    collect_ignore_glob = ["tests/test_gui_*.py"]


@pytest.fixture(autouse=True)
def keine_modalen_dialoge(monkeypatch):
    """Ersetzt alle messagebox-Dialoge durch Attrappen.

    Ohne das koennte ein Test an einem echten, blockierenden Dialog haengen
    bleiben (die GUI wird ohne Fenster instanziiert). Einzelne Tests duerfen
    die Attrappen danach gezielt ueberschreiben.

    Fehlt tkinter, wird die GUI nicht geladen; die reinen Nicht-GUI-Tests
    laufen dann unveraendert weiter, die GUI-Tests sind bereits ueber
    ``collect_ignore_glob`` ausgenommen.
    """
    try:
        import gui
    except Exception:  # pragma: no cover - nur ohne tkinter
        return

    def still(*args, **kwargs):
        return None

    for name in ("showinfo", "showwarning", "showerror"):
        monkeypatch.setattr(gui.messagebox, name, still)
    monkeypatch.setattr(gui.messagebox, "askyesno", lambda *a, **k: False)
    monkeypatch.setattr(gui.messagebox, "askokcancel", lambda *a, **k: False)
