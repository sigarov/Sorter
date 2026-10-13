"""Tests fuer das gemeinsame Einsammeln der Dateien (MediaWorker)."""

import os
import queue
import threading

from dedup_sorter import DedupSorter
from sorter import Sorter
from translations import TRANSLATIONS

LANG = TRANSLATIONS["de"]


def _sorter(quelle, ziel, filter_=None):
    return Sorter(
        str(quelle),
        "",
        filter_ or [],
        [],
        str(ziel),
        True,
        False,
        False,
        "year",
        "original",
        LANG,
        queue.Queue(),
        threading.Event(),
    )


def _dedup(ziel, filter_=None):
    return DedupSorter(str(ziel), True, False, LANG, queue.Queue(), threading.Event())


def _datei(pfad):
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_bytes(b"x")


def test_sammelt_medien_und_liefert_laufwerk(tmp_path):
    q = tmp_path / "q"
    _datei(q / "a.jpg")
    _datei(q / "b.mp4")
    _datei(q / "notiz.txt")
    _datei(q / "_index.txt")

    alle = _sorter(q, tmp_path / "z").sammle_dateien(mit_laufwerk=True)

    assert sorted(os.path.basename(p) for p, _lw in alle) == ["a.jpg", "b.mp4"]
    assert {lw for _p, lw in alle} == {str(q)}


def test_ueberspringt_duplikate_ordner(tmp_path):
    q = tmp_path / "q"
    _datei(q / "a.jpg")
    _datei(q / "Duplicates" / "a_1.jpg")

    assert [os.path.basename(p) for p in _dedup(q).sammle_dateien()] == ["a.jpg"]


def test_ueberspringt_den_alten_duplikate_ordner(tmp_path):
    """Bestaende aus alten Laeufen (_Duplikate) duerfen nicht neu einsortiert werden."""
    q = tmp_path / "q"
    _datei(q / "a.jpg")
    _datei(q / "_Duplikate" / "a_1.jpg")

    assert [os.path.basename(p) for p in _dedup(q).sammle_dateien()] == ["a.jpg"]


def test_dupes_ordner_name_und_helfer():
    from config import DUPES_FOLDER, ist_dupes_ordner

    assert DUPES_FOLDER == "Duplicates"
    assert ist_dupes_ordner("Duplicates") is True
    assert ist_dupes_ordner("_Duplikate") is True
    assert ist_dupes_ordner("Bilder") is False


def test_sorter_ueberspringt_zielordner(tmp_path):
    q = tmp_path / "q"
    z = q / "Sorted"
    _datei(q / "a.jpg")
    _datei(z / "b.jpg")

    assert [os.path.basename(p) for p in _sorter(q, z).sammle_dateien()] == ["a.jpg"]


def test_filter_nach_ordnernamen(tmp_path):
    q = tmp_path / "q"
    _datei(q / "Fotos" / "a.jpg")
    _datei(q / "Sonstiges" / "b.jpg")

    gefunden = _sorter(q, tmp_path / "z", filter_=["fotos"]).sammle_dateien()

    assert [os.path.basename(p) for p in gefunden] == ["a.jpg"]


def test_filter_behaelt_unterordner(tmp_path):
    q = tmp_path / "q"
    _datei(q / "Fotos" / "2020" / "a.jpg")
    _datei(q / "Sonstiges" / "b.jpg")

    gefunden = _sorter(q, tmp_path / "z", filter_=["fotos"]).sammle_dateien()

    assert [os.path.basename(p) for p in gefunden] == ["a.jpg"]
