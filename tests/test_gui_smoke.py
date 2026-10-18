"""Smoke-Test: die vollstaendige GUI einmal aufbauen und wieder schliessen.

Die uebrigen GUI-Tests arbeiten mit ``App.__new__`` und Attrappen. Dieser Test
prueft zusaetzlich, dass der echte Aufbau in der richtigen Reihenfolge
funktioniert (Widgets, Sprache, Dedup-Freigabe).
"""

import gc
import tkinter as tk

import pytest

import gui


@pytest.fixture
def app(monkeypatch, tmp_path):
    monkeypatch.setattr(gui.App, "_settings_path", lambda self: str(tmp_path / "settings.json"))
    try:
        root = gui.App()
    except tk.TclError as exc:
        pytest.skip(f"Kein Tk-Display verfuegbar: {exc}")
    try:
        yield root
    finally:
        root.destroy()
        # Tk-Variablen erst jetzt freigeben, damit sie nicht waehrend eines
        # spaeteren Tests am zerstoerten Interpreter scheitern.
        del root
        gc.collect()


def test_app_baut_alle_widgets_auf(app):
    assert app.grp_general.winfo_exists()
    assert app.grp_dedup.winfo_exists()
    assert app.grp_naming.winfo_exists()
    assert app.nb.index("end") == 2
    assert app.nb.index(app.nb.select()) == 0
    assert app.btn_start.cget("state") == "normal"
    assert app.btn_stop.cget("state") == "disabled"
    assert app.progress["value"] == 0
    assert app.progress_index["value"] == 0
    assert app.txt.winfo_exists()


def test_sprachwechsel_aktualisiert_die_beschriftungen(app):
    app.lang_display.set(gui.TRANSLATIONS["en"]["name"])
    app._on_lang_change()

    assert app.lang_code == "en"
    assert app.btn_start.cget("text") == gui.TRANSLATIONS["en"]["btn_start"]
    assert app.chk_dry.cget("text") == gui.TRANSLATIONS["en"]["chk_dryrun"]
    assert app.grp_naming.cget("text") == gui.TRANSLATIONS["en"]["lbl_group_naming"]


def test_dedup_tab_ist_ohne_sortierlauf_gesperrt(app, tmp_path):
    app.ziel.set(str(tmp_path))
    app._aktualisiere_dedup_freigabe()

    assert app.dedup.get() is False
    assert app.nb.tab(1, "text") == gui.TRANSLATIONS["de"]["mode_dedup_locked"]

    (tmp_path / "_index.txt").write_text("", encoding="utf-8")
    app._aktualisiere_dedup_freigabe()

    assert app.nb.tab(1, "text") == gui.TRANSLATIONS["de"]["mode_dedup"]


def test_dedup_modus_sperrt_quellen_und_laesst_das_ziel_offen(app, tmp_path):
    (tmp_path / "_index.txt").write_text("", encoding="utf-8")
    app.ziel.set(str(tmp_path))
    app.dedup.set(True)
    app._on_dedup_toggle()

    assert app.q1_entry.cget("state") == "disabled"
    assert app.q2_entry.cget("state") == "disabled"
    assert app.filter1_entry.cget("state") == "disabled"
    assert app.btn_w1.cget("state") == "disabled"
    assert app.ziel_entry.cget("state") == "normal"
    assert app.btn_w3.cget("state") == "normal"
    assert (
        app._text_widgets["lbl_target"].cget("text") == gui.TRANSLATIONS["de"]["lbl_target_dedup"]
    )


def test_tab_ist_der_einzige_dedup_schalter(app, tmp_path):
    (tmp_path / "_index.txt").write_text("", encoding="utf-8")
    app.ziel.set(str(tmp_path))

    app.nb.select(1)
    app.update()

    assert app.dedup.get() is True
    assert app.q1_entry.cget("state") == "disabled"
    assert app.nb.tab(1, "text") == gui.TRANSLATIONS["de"]["mode_dedup"]

    app.nb.select(0)
    app.update()

    assert app.dedup.get() is False
    assert app.q1_entry.cget("state") == "normal"
