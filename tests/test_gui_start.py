"""Tests fuer Startpruefungen, Fenstergeometrie und Vorschau der GUI."""

import pytest

import gui


class _Var:
    """Minimaler Ersatz fuer ein tk.StringVar/BooleanVar."""

    def __init__(self, wert=""):
        self._wert = wert

    def get(self):
        return self._wert

    def set(self, wert):
        self._wert = wert


def _app(q1="", q2="", ziel="", dedup=False, force=False, lang=None):
    from translations import TRANSLATIONS

    app = gui.App.__new__(gui.App)
    app.lang = lang if lang is not None else TRANSLATIONS["de"]
    app.q1, app.q2, app.ziel = _Var(q1), _Var(q2), _Var(ziel)
    app.filter1, app.filter2 = _Var(), _Var()
    app.dedup, app.dedup_force = _Var(dedup), _Var(force)
    return app


# ---------- Startpruefungen ----------
def test_start_ohne_quelle_warnt(monkeypatch):
    app = _app()
    warnungen = []
    monkeypatch.setattr(gui.messagebox, "showwarning", lambda *a: warnungen.append(a))

    assert app._bestaetige_start() is False
    assert warnungen, "ohne Quelle muss gewarnt werden"


def test_start_sortieren_ohne_ziel_warnt(monkeypatch):
    app = _app(q1="C:/quelle")
    monkeypatch.setattr(gui.messagebox, "showwarning", lambda *a: None)

    assert app._bestaetige_start() is False


def test_start_sortieren_fragt_die_vorschau(monkeypatch):
    app = _app(q1="C:/quelle", ziel="C:/ziel")
    monkeypatch.setattr(gui.messagebox, "showwarning", lambda *a: pytest.fail("keine Warnung"))
    gerufen = []
    monkeypatch.setattr(app, "_confirm_preview", lambda f1, f2: gerufen.append((f1, f2)) or True)

    assert app._bestaetige_start() is True
    assert gerufen == [([], [])]


def test_start_dedup_ohne_ziel_warnt(monkeypatch):
    app = _app(dedup=True)
    warnungen = []
    monkeypatch.setattr(gui.messagebox, "showwarning", lambda *a: warnungen.append(a))

    assert app._bestaetige_start() is False
    assert warnungen, "im Dedup-Modus muss ein Ziel gewaehlt sein"


def test_start_dedup_ohne_sortierlauf_zeigt_hinweis(monkeypatch, tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir()  # noch keine _index.txt
    app = _app(ziel=str(ziel), dedup=True)
    monkeypatch.setattr(gui.messagebox, "showwarning", lambda *a: pytest.fail("keine Warnung"))
    hinweise = []
    monkeypatch.setattr(gui.messagebox, "showinfo", lambda *a: hinweise.append(a))

    assert app._bestaetige_start() is False
    assert hinweise, "ohne Sortierlauf muss erklaert werden, warum nicht"


def test_start_dedup_nach_sortierlauf_erlaubt(monkeypatch, tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    (ziel / "_index.txt").write_text("# Index", encoding="utf-8")
    app = _app(ziel=str(ziel), dedup=True, force=False)
    monkeypatch.setattr(gui.messagebox, "showwarning", lambda *a: pytest.fail("keine Warnung"))
    monkeypatch.setattr(gui.messagebox, "showinfo", lambda *a: pytest.fail("kein Hinweis"))
    monkeypatch.setattr(gui.messagebox, "askyesno", lambda *a: pytest.fail("nicht nachfragen"))

    assert app._bestaetige_start() is True


def test_start_dedup_im_sorted_unterordner_erlaubt(monkeypatch, tmp_path):
    """Quelle = Ziel beim Sortieren -> der Index liegt in '<Ziel>/Sorted'."""
    ziel = tmp_path / "ziel"
    (ziel / "Sorted").mkdir(parents=True)
    (ziel / "Sorted" / "_index.txt").write_text("# Index", encoding="utf-8")
    app = _app(ziel=str(ziel), dedup=True)
    monkeypatch.setattr(gui.messagebox, "showwarning", lambda *a: pytest.fail("keine Warnung"))
    monkeypatch.setattr(gui.messagebox, "showinfo", lambda *a: pytest.fail("kein Hinweis"))

    assert app._bestaetige_start() is True
    assert app._dedup_ziel() == str(ziel / "Sorted")


def test_start_dedup_ignoriert_quellen(monkeypatch, tmp_path):
    """Ohne Quellen ist Dedup erlaubt – das Ziel allein zaehlt."""
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    (ziel / "_index.txt").write_text("# Index", encoding="utf-8")
    app = _app(q1="", q2="", ziel=str(ziel), dedup=True)

    assert app._bestaetige_start() is True


def test_start_force_verlangt_bestaetigung(monkeypatch, tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    (ziel / "_index.txt").write_text("# Index", encoding="utf-8")
    app = _app(ziel=str(ziel), dedup=True, force=True)
    gefragt = []
    monkeypatch.setattr(
        gui.messagebox, "askyesno", lambda titel, text: gefragt.append((titel, text)) or True
    )

    assert app._bestaetige_start() is True
    assert gefragt, "im Force-Modus muss nachgefragt werden"


def test_start_force_abbruch_bricht_ab(monkeypatch, tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    (ziel / "_index.txt").write_text("# Index", encoding="utf-8")
    app = _app(ziel=str(ziel), dedup=True, force=True)
    monkeypatch.setattr(gui.messagebox, "askyesno", lambda titel, text: False)

    assert app._bestaetige_start() is False


def test_start_ohne_force_fragt_nicht(monkeypatch, tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    (ziel / "_index.txt").write_text("# Index", encoding="utf-8")
    app = _app(ziel=str(ziel), dedup=True, force=False)
    monkeypatch.setattr(gui.messagebox, "askyesno", lambda *a: pytest.fail("nicht nachfragen"))
    monkeypatch.setattr(gui.messagebox, "showwarning", lambda *a: pytest.fail("keine Warnung"))

    assert app._bestaetige_start() is True


# ---------- Dedup-Freigabe ----------
def test_dedup_freigabe_ohne_ziel():
    app = _app()

    assert app._dedup_freigabe() is False
    assert app._dedup_ziel() is None


def test_dedup_freigabe_ohne_index(tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    app = _app(ziel=str(ziel))

    assert app._dedup_freigabe() is False
    assert app._dedup_ziel() == str(ziel), "ohne Index bleibt das Ziel der Vorschlag"


def test_dedup_freigabe_mit_index(tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    (ziel / "_index.txt").write_text("# Index", encoding="utf-8")
    app = _app(ziel=str(ziel))

    assert app._dedup_freigabe() is True
    assert app._dedup_ziel() == str(ziel)


def test_aktualisiere_freigabe_nimmt_modus_zurueck(monkeypatch, tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    app = _app(ziel=str(ziel), dedup=True)
    app.dedup.set(True)
    umgeschaltet = []
    monkeypatch.setattr(app, "_on_dedup_toggle", lambda: umgeschaltet.append(True))

    assert app._aktualisiere_dedup_freigabe() is False
    assert app.dedup.get() is False, "ohne Freigabe darf Dedup nicht aktiv bleiben"
    assert umgeschaltet


def test_aktualisiere_freigabe_laesst_modus_stehen(monkeypatch, tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    (ziel / "_index.txt").write_text("# Index", encoding="utf-8")
    app = _app(ziel=str(ziel), dedup=True)
    app.dedup.set(True)
    monkeypatch.setattr(app, "_on_dedup_toggle", lambda: pytest.fail("nicht umschalten"))

    assert app._aktualisiere_dedup_freigabe() is True
    assert app.dedup.get() is True


def test_tab_titel_zeigt_gesperrt(tmp_path):
    class _Nb:
        def __init__(self):
            self.titel = {}

        def tab(self, idx, text=None):
            self.titel[idx] = text

    ziel = tmp_path / "ziel"
    ziel.mkdir()
    app = _app(ziel=str(ziel))
    app.nb = _Nb()

    app._setze_tab_titel(False)
    assert "gesperrt" in app.nb.titel[1]

    app._setze_tab_titel(True)
    assert "gesperrt" not in app.nb.titel[1]


# ---------- Fenstergeometrie ----------
def test_geometry_zerlegen():
    app = gui.App.__new__(gui.App)

    assert app._geometry_zerlegen("920x800+10+20") == (920, 800, 10, 20)
    assert app._geometry_zerlegen("920x800-10-20") == (920, 800, -10, -20)
    assert app._geometry_zerlegen("kaputt") is None


def test_geometrie_passt_gegen_bildschirmgroesse():
    app = gui.App.__new__(gui.App)
    app.winfo_screenwidth = lambda: 1920
    app.winfo_screenheight = lambda: 1080

    assert app._geometrie_passt("920x800+10+10") is True
    assert app._geometrie_passt("900x800+1500+10") is False, "rechts ausserhalb"
    assert app._geometrie_passt("900x1200+10+10") is False, "zu hoch"
    assert app._geometrie_passt("3000x800+0+0") is False, "zu breit"
    assert app._geometrie_passt("920x800-10-10") is True, "am rechten Rand verankert"
    assert app._geometrie_passt("quatsch") is False


# ---------- Vorschau ----------
_TEMPLATE = {"preview_msg": "{n}|{size}|{src}|{dst}", "preview_title": "T"}


def test_vorschau_zeigt_alle_quellen_und_das_ziel(monkeypatch, tmp_path):
    q1, q2 = tmp_path / "eins", tmp_path / "zwei"
    q1.mkdir()
    q2.mkdir()
    (q1 / "a.jpg").write_bytes(b"a")
    (q2 / "b.jpg").write_bytes(b"b")
    app = _app(q1=str(q1), q2=str(q2), ziel=str(tmp_path / "ziel"), lang=_TEMPLATE)
    gesehen = {}
    monkeypatch.setattr(
        gui.messagebox, "askokcancel", lambda titel, text: gesehen.update(text=text) or True
    )

    app._confirm_preview([], [])

    assert str(q1) in gesehen["text"]
    assert str(q2) in gesehen["text"]


def test_vorschau_zeigt_sorted_wenn_quelle_gleich_ziel(monkeypatch, tmp_path):
    q = tmp_path / "q"
    q.mkdir()
    (q / "a.jpg").write_bytes(b"a")
    app = _app(q1=str(q), ziel=str(q), lang=_TEMPLATE)
    gesehen = {}
    monkeypatch.setattr(
        gui.messagebox, "askokcancel", lambda titel, text: gesehen.update(text=text) or True
    )

    app._confirm_preview([], [])

    assert "Sorted" in gesehen["text"]


def test_vorschau_zaehlt_duplikate_ordner_nicht_mit(monkeypatch, tmp_path):
    q = tmp_path / "q"
    (q / "Duplicates").mkdir(parents=True)
    (q / "a.jpg").write_bytes(b"a")
    (q / "Duplicates" / "a_1.jpg").write_bytes(b"a")
    app = _app(q1=str(q), ziel=str(tmp_path / "z"), lang=_TEMPLATE)
    gesehen = {}
    monkeypatch.setattr(
        gui.messagebox, "askokcancel", lambda titel, text: gesehen.update(text=text) or True
    )

    app._confirm_preview([], [])

    assert gesehen["text"].startswith("1|"), gesehen["text"]
