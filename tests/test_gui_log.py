"""Tests fuer die Log-Begrenzung der GUI (ohne echtes Tk-Fenster)."""

import gui


class _FakeText:
    def __init__(self, letzte_zeile):
        self._letzte_zeile = letzte_zeile
        self.geloescht = []

    def index(self, _spec):
        return self._letzte_zeile

    def delete(self, start, ende):
        self.geloescht.append((start, ende))


def _app(text):
    app = gui.App.__new__(gui.App)
    app.txt = text
    return app


def test_trim_log_text_kuerzt_bei_zu_vielen_zeilen():
    app = _app(_FakeText("100000.0"))
    app._trim_log_text()
    assert app.txt.geloescht == [("1.0", f"{gui.MAX_LOG_ZEILEN // 4}.0")]


def test_trim_log_text_laesst_kurzes_log_unberuehrt():
    app = _app(_FakeText("10.0"))
    app._trim_log_text()
    assert app.txt.geloescht == []
