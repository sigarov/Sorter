"""Tests fuer das Merken der zuletzt gewaehlten Ordner-Pfade."""

import gui
from translations import TRANSLATIONS


class _Var:
    """Minimaler Ersatz fuer ein tk.StringVar."""

    def __init__(self, wert=""):
        self._wert = wert

    def get(self):
        return self._wert

    def set(self, wert):
        self._wert = wert


def _app():
    """App ohne Tk-Fenster; Speichern wird nicht angefasst."""
    app = gui.App.__new__(gui.App)
    app.q1 = _Var()
    app.q2 = _Var()
    app.ziel = _Var()
    app._last_paths = {}
    app.gespeichert = 0

    def merken():
        app.gespeichert += 1

    app._remember_paths = merken
    return app


def test_pfad_felder_sind_die_einzige_quelle():
    app = _app()

    assert [k for k, _v in app._pfad_felder()] == ["q1", "q2", "ziel"]
    assert app._feld_key(app.q2) == "q2"
    assert app._feld_key(_Var()) is None


def test_waehle_oeffnet_im_gemerkten_ordner(monkeypatch, tmp_path):
    app = _app()
    letzter = tmp_path / "letzter_ordner"
    letzter.mkdir()
    app._last_paths["q1"] = str(letzter)
    aufrufe = []
    monkeypatch.setattr(gui.filedialog, "askdirectory", lambda **kw: aufrufe.append(kw) or "")

    app.waehle(app.q1)

    assert aufrufe[0]["initialdir"] == str(letzter)


def test_waehle_faellt_auf_den_feldinhalt_zurueck(monkeypatch, tmp_path):
    app = _app()
    eingetragen = tmp_path / "eingetragen"
    eingetragen.mkdir()
    app.q2.set(str(eingetragen))
    aufrufe = []
    monkeypatch.setattr(gui.filedialog, "askdirectory", lambda **kw: aufrufe.append(kw) or "")

    app.waehle(app.q2)

    assert aufrufe[0]["initialdir"] == str(eingetragen)


def test_waehle_ohne_gemerkten_ordner_ohne_initialdir(monkeypatch):
    app = _app()
    aufrufe = []
    monkeypatch.setattr(gui.filedialog, "askdirectory", lambda **kw: aufrufe.append(kw) or "")

    app.waehle(app.ziel)

    assert aufrufe == [{}], "ohne bekannten Ordner darf kein initialdir gesetzt sein"


def test_waehle_merkt_pfad_unter_dem_feld_schluessel(monkeypatch, tmp_path):
    app = _app()
    gewaehlt = tmp_path / "gewaehlt"
    gewaehlt.mkdir()
    monkeypatch.setattr(gui.filedialog, "askdirectory", lambda **kw: str(gewaehlt))

    app.waehle(app.ziel)

    assert app.ziel.get() == str(gewaehlt)
    assert app._last_paths["ziel"] == str(gewaehlt)
    assert "target" not in app._last_paths, "alter Schluessel darf nicht mehr benutzt werden"
    assert app.gespeichert == 1


def test_load_settings_laedt_pfade_in_die_feld_schluessel(monkeypatch, tmp_path):
    datei = tmp_path / "settings.json"
    datei.write_text(
        '{"last_paths": {"q1": "C:/eins", "q2": "C:/zwei", "ziel": "C:/drei"}}', encoding="utf-8"
    )
    app = _app()
    app._settings = {}
    app.lang_code = "de"
    app.lang = TRANSLATIONS["de"]
    monkeypatch.setattr(app, "_settings_path", lambda: str(datei))

    app._load_settings()

    assert app._last_paths["q1"] == "C:/eins"
    assert app._last_paths["q2"] == "C:/zwei"
    assert app._last_paths["ziel"] == "C:/drei"
