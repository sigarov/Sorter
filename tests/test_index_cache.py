"""Tests fuer den Hash-Cache, den der Trockenlauf fuer den Echtlauf anlegt."""

import os
import queue
import threading

import pytest

import sorter as sorter_mod
from sorter import Sorter
from translations import TRANSLATIONS


def _lauf(quelle, ziel, **kw):
    lq = queue.Queue()
    ev = threading.Event()
    args = dict(
        quelle1=str(quelle),
        quelle2="",
        ordner1=[],
        ordner2=[],
        ziel=str(ziel),
        trockenlauf=False,
        skip_existing=False,
        gemeinsam=True,
        granularitaet="year",
        naming="original",
        lang=TRANSLATIONS["de"],
        log_queue=lq,
        stop_event=ev,
    )
    args.update(kw)
    s = Sorter(**args)
    s.start()
    s.join(60)
    assert not s.is_alive(), "Sorter-Thread haengt"
    return s


def _texte(lq):
    texte = []
    while not lq.empty():
        tag, wert = lq.get()
        if tag not in ("index", "sort_progress") and isinstance(wert, str):
            texte.append(wert)
    return texte


@pytest.fixture
def app_verzeichnis(tmp_path, monkeypatch):
    """Lenkt den Cache in ein temporaeres App-Verzeichnis."""
    app = tmp_path / "app"
    monkeypatch.setattr(sorter_mod, "app_dir", lambda: str(app))
    return app


def _zaehle_hashes(monkeypatch):
    """Erfasst, welche Pfade tatsaechlich gehasht werden."""
    gehasht = []
    original = sorter_mod.hash_datei

    def zaehlend(pfad, *args, **kwargs):
        gehasht.append(os.path.normcase(str(pfad)))
        return original(pfad, *args, **kwargs)

    monkeypatch.setattr(sorter_mod, "hash_datei", zaehlend)
    return gehasht


def test_trockenlauf_legt_cache_aber_keinen_index_an(app_verzeichnis, tmp_path):
    q = tmp_path / "q"
    z = tmp_path / "z"
    q.mkdir()
    z.mkdir()
    (z / "alt.jpg").write_bytes(b"ALT")
    (q / "neu_20200102.jpg").write_bytes(b"NEU")

    s = _lauf(q, z, trockenlauf=True)

    assert not (z / "_index.txt").exists(), "Trockenlauf darf den Dedup-Marker nicht anlegen"
    cache = s._index_cache_pfad()
    assert cache.exists()
    inhalt = cache.read_text(encoding="utf-8")
    assert inhalt.startswith("# MedienSortierer Index-Cache v1")
    assert "alt.jpg" in inhalt
    assert "neu_20200102.jpg" not in inhalt, "Quelldateien gehoeren nicht in den Ziel-Cache"


def test_echt_lauf_nutzt_cache_und_entfernt_ihn(app_verzeichnis, tmp_path, monkeypatch):
    q = tmp_path / "q"
    z = tmp_path / "z"
    q.mkdir()
    z.mkdir()
    alt = z / "alt.jpg"
    alt.write_bytes(b"ALT")
    neu = q / "neu_20200102.jpg"
    neu.write_bytes(b"NEU")

    dry = _lauf(q, z, trockenlauf=True)
    cache = dry._index_cache_pfad()
    assert cache.exists()

    gehasht = _zaehle_hashes(monkeypatch)
    echt = _lauf(q, z)

    assert os.path.normcase(str(alt)) not in gehasht, "Zieldatei muss aus dem Cache kommen"
    assert os.path.normcase(str(neu)) in gehasht, "Quelldatei muss geprueft werden"
    assert echt.stat["neu"] == 1
    assert (z / "_index.txt").exists()
    assert not cache.exists(), "nach dem Echtlauf ist der Trockenlauf-Cache ueberfluessig"


def test_echt_lauf_erkennt_duplikat_trotz_cache(app_verzeichnis, tmp_path):
    q = tmp_path / "q"
    z = tmp_path / "z"
    q.mkdir()
    z.mkdir()
    (z / "vorhanden.jpg").write_bytes(b"GLEICH")
    (q / "quelle_20200102.jpg").write_bytes(b"GLEICH")

    _lauf(q, z, trockenlauf=True)
    s = _lauf(q, z)

    assert s.stat["dup"] == 1
    assert s.stat["neu"] == 0
    assert (z / "vorhanden.jpg").exists()
    assert not (z / "2020").exists(), "es darf nichts kopiert worden sein"


def test_geaenderte_zieldatei_wird_neu_gehasht(app_verzeichnis, tmp_path, monkeypatch):
    q = tmp_path / "q"
    z = tmp_path / "z"
    q.mkdir()
    z.mkdir()
    alt = z / "alt.jpg"
    alt.write_bytes(b"ALT")
    (q / "neu_20200102.jpg").write_bytes(b"NEU")

    _lauf(q, z, trockenlauf=True)
    alt.write_bytes(b"ALT-NEU")  # andere Groesse -> Cache-Eintrag ist ungueltig

    gehasht = _zaehle_hashes(monkeypatch)
    _lauf(q, z)

    assert os.path.normcase(str(alt)) in gehasht


def test_kaputter_cache_wird_ignoriert(app_verzeichnis, tmp_path):
    q = tmp_path / "q"
    z = tmp_path / "z"
    q.mkdir()
    z.mkdir()
    (z / "alt.jpg").write_bytes(b"ALT")
    (q / "neu_20200102.jpg").write_bytes(b"NEU")

    dry = _lauf(q, z, trockenlauf=True)
    dry._index_cache_pfad().write_text("kaputt\n", encoding="utf-8")

    s = _lauf(q, z)

    assert s.stat["neu"] == 1
    assert (z / "2020" / "neu_20200102.jpg").exists()


def test_cache_ist_pro_ziel_getrennt(app_verzeichnis, tmp_path):
    q1 = tmp_path / "q1"
    q2 = tmp_path / "q2"
    z1 = tmp_path / "z1"
    z2 = tmp_path / "z2"
    for p in (q1, q2, z1, z2):
        p.mkdir()
    (q1 / "a_20200102.jpg").write_bytes(b"A")
    (q2 / "b_20200102.jpg").write_bytes(b"B")

    s1 = _lauf(q1, z1, trockenlauf=True)
    s2 = _lauf(q2, z2, trockenlauf=True)

    assert s1._index_cache_pfad() != s2._index_cache_pfad()


def test_cache_meldet_treffer_im_log(app_verzeichnis, tmp_path):
    q = tmp_path / "q"
    z = tmp_path / "z"
    q.mkdir()
    z.mkdir()
    (z / "alt.jpg").write_bytes(b"ALT")
    (q / "neu_20200102.jpg").write_bytes(b"NEU")

    _lauf(q, z, trockenlauf=True)
    lq = queue.Queue()
    _lauf(q, z, log_queue=lq)
    texte = "\n".join(_texte(lq))

    assert "Trockenlauf-Cache geladen" in texte
