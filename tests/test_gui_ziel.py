"""Tests fuer die Ziel-Umleitung, wenn Quelle und Ziel identisch sind."""

import os

import gui
from config import SORT_UNTERORDNER


class _Var:
    """Minimaler Ersatz fuer ein tk.StringVar (nur get())."""

    def __init__(self, wert=""):
        self._wert = wert

    def get(self):
        return self._wert


def _app(q1, q2, ziel):
    app = gui.App.__new__(gui.App)
    app.q1 = _Var(q1)
    app.q2 = _Var(q2)
    app.ziel = _Var(ziel)
    return app


def test_konstante_heisst_sorted():
    assert SORT_UNTERORDNER == "Sorted"


def test_quelle_gleich_ziel_leitet_in_sorted_um(tmp_path):
    app = _app(str(tmp_path), "", str(tmp_path))

    ziel, umgeleitet = app._effektives_ziel()

    assert umgeleitet is True
    assert ziel == os.path.join(str(tmp_path), "Sorted")
    assert os.path.basename(ziel) == "Sorted"


def test_zweite_quelle_gleich_ziel_leitet_ebenfalls_um(tmp_path):
    app = _app(str(tmp_path / "andere"), str(tmp_path), str(tmp_path))

    ziel, umgeleitet = app._effektives_ziel()

    assert umgeleitet is True
    assert os.path.basename(ziel) == "Sorted"


def test_unterschiedliche_ordner_werden_nicht_umgeleitet(tmp_path):
    app = _app(str(tmp_path / "q"), "", str(tmp_path / "z"))

    ziel, umgeleitet = app._effektives_ziel()

    assert umgeleitet is False
    assert ziel == str(tmp_path / "z")
