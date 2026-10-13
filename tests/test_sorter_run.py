"""Ende-zu-Ende-Tests fuer einen kompletten Sorter-Durchlauf."""

import queue
import threading

import pytest

import sorter as sorter_mod
from sorter import Sorter
from translations import TRANSLATIONS


def _lauf(quelle, ziel, **kw):
    """Startet den Sorter mit den Test-Vorgaben und wartet auf das Ende."""
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
        gemeinsam=False,
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


def test_sortiert_dateien_in_jahresordner(tmp_path):
    q = tmp_path / "q"
    q.mkdir()
    (q / "IMG_20200102_1.jpg").write_bytes(b"a" * 10)
    (q / "IMG_20210503_2.png").write_bytes(b"b" * 20)
    z = tmp_path / "z"

    s = _lauf(q, z, gemeinsam=True)

    assert s.stat["neu"] == 2
    assert s.stat["fehler"] == 0
    assert (z / "2020" / "IMG_20200102_1.jpg").read_bytes() == b"a" * 10
    assert (z / "2021" / "IMG_20210503_2.png").read_bytes() == b"b" * 20


def test_trennt_bilder_und_videos(tmp_path):
    q = tmp_path / "q"
    q.mkdir()
    (q / "IMG_20200102_1.jpg").write_bytes(b"a" * 10)
    (q / "clip_20210503.mp4").write_bytes(b"v" * 20)
    z = tmp_path / "z"

    s = _lauf(q, z)

    assert s.stat["neu"] == 2
    assert (z / "Pictures" / "2020" / "IMG_20200102_1.jpg").exists()
    assert (z / "Videos" / "2021" / "clip_20210503.mp4").exists()


@pytest.mark.parametrize("code", list(TRANSLATIONS))
def test_ordnernamen_sind_immer_englisch(tmp_path, code):
    """Die Ordnerstruktur haengt nicht von der GUI-Sprache ab."""
    q = tmp_path / code / "q"
    q.mkdir(parents=True)
    (q / "IMG_20200102_1.jpg").write_bytes(b"a")
    (q / "clip_20200102.mp4").write_bytes(b"v")
    (q / "ohne_datum.jpg").write_bytes(b"o")
    z = tmp_path / code / "z"

    _lauf(q, z, lang=TRANSLATIONS[code])

    assert (z / "Pictures" / "2020" / "IMG_20200102_1.jpg").exists()
    assert (z / "Videos" / "2020" / "clip_20200102.mp4").exists()
    assert (z / "_No_Date" / "Pictures" / "ohne_datum.jpg").exists()


def test_bricht_ab_wenn_zu_wenig_platz(monkeypatch, tmp_path):
    q = tmp_path / "q"
    q.mkdir()
    (q / "IMG_20200102_1.jpg").write_bytes(b"a" * 1000)
    z = tmp_path / "z"
    monkeypatch.setattr(sorter_mod, "freier_platz", lambda _pfad: 1)

    s = _lauf(q, z)

    assert s.stat["neu"] == 0
    assert s.stat["fehler"] == 1
    assert list(z.iterdir()) == [], "es darf nichts kopiert worden sein"


def test_liegen_gebliebene_tmp_dateien_zaehlen_nicht_als_duplikat(tmp_path):
    """Eine abgebrochene Kopie (.tmp) im Ziel darf keine Quelle blockieren."""
    q = tmp_path / "q"
    z = tmp_path / "z"
    q.mkdir()
    z.mkdir()
    (z / "foto.jpg").write_bytes(b"AAA")
    (z / "abgebrochen.jpg.tmp").write_bytes(b"BBB")
    (q / "quell_20200102.jpg").write_bytes(b"BBB")

    s = _lauf(q, z, gemeinsam=True)

    assert s.stat["dup"] == 0, "die .tmp-Datei darf nicht als Duplikat gelten"
    assert s.stat["neu"] == 1
    assert (z / "2020" / "quell_20200102.jpg").read_bytes() == b"BBB"
    assert (z / "abgebrochen.jpg.tmp").exists(), "fremde .tmp-Dateien nicht anfassen"


def test_aussortierte_dateien_blockieren_keine_quelle(tmp_path):
    """Der Duplicates-Ordner im Ziel gehoert nicht in den Index."""
    q = tmp_path / "q"
    z = tmp_path / "z"
    q.mkdir()
    (z / "Duplicates").mkdir(parents=True)
    (z / "foto.jpg").write_bytes(b"AAA")
    (z / "Duplicates" / "aussortiert.jpg").write_bytes(b"BBB")
    (q / "quell_20200102.jpg").write_bytes(b"BBB")

    s = _lauf(q, z, gemeinsam=True)

    assert s.stat["dup"] == 0, "aussortierter Inhalt darf nicht als vorhanden gelten"
    assert s.stat["neu"] == 1
    assert (z / "2020" / "quell_20200102.jpg").exists()
