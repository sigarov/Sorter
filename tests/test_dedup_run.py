"""Ende-zu-Ende-Tests fuer einen DedupSorter-Durchlauf."""

import queue
import threading

from dedup_sorter import DedupSorter
from translations import TRANSLATIONS


def _lauf(ziel, trockenlauf=False, force=False):
    lq = queue.Queue()
    ev = threading.Event()
    s = DedupSorter(str(ziel), trockenlauf, force, TRANSLATIONS["de"], lq, ev)
    s.start()
    s.join(60)
    assert not s.is_alive(), "DedupSorter-Thread haengt"
    return s


def test_verschiebt_identisches_duplikat(tmp_path):
    q = tmp_path / "q"
    q.mkdir()
    (q / "a.jpg").write_bytes(b"gleich")
    (q / "a_1.jpg").write_bytes(b"gleich")

    s = _lauf(q)

    assert s.stat["verschoben"] == 1
    assert s.stat["unterschiedlich"] == 0
    assert not (q / "a_1.jpg").exists()
    assert (q / "Duplicates" / "a_1.jpg").exists()
    assert (q / "a.jpg").exists(), "Original bleibt liegen"


def test_behaelt_abweichendes_duplikat(tmp_path):
    q = tmp_path / "q"
    q.mkdir()
    (q / "a.jpg").write_bytes(b"eins")
    (q / "a_1.jpg").write_bytes(b"zwei")

    s = _lauf(q)

    assert s.stat["verschoben"] == 0
    assert s.stat["unterschiedlich"] == 1
    assert (q / "a_1.jpg").exists()


def test_trockenlauf_aendert_nichts(tmp_path):
    q = tmp_path / "q"
    q.mkdir()
    (q / "a.jpg").write_bytes(b"gleich")
    (q / "a_1.jpg").write_bytes(b"gleich")

    s = _lauf(q, trockenlauf=True)

    assert s.stat["verschoben"] == 1
    assert (q / "a_1.jpg").exists()
    assert not (q / "Duplicates").exists()


def test_arbeitet_nur_im_ziel_und_laesst_die_quelle_in_ruhe(tmp_path):
    """Dedup laeuft ausschliesslich im Zielordner (Ergebnis des Sortierlaufs)."""
    quelle = tmp_path / "quelle"
    ziel = tmp_path / "ziel"
    (quelle / "2020").mkdir(parents=True)
    (ziel / "2020").mkdir(parents=True)
    # In der Quelle liegt ebenfalls ein Kandidat - er darf nicht angefasst werden.
    (quelle / "a.jpg").write_bytes(b"gleich")
    (quelle / "a_1.jpg").write_bytes(b"gleich")
    (ziel / "a.jpg").write_bytes(b"gleich")
    (ziel / "a_1.jpg").write_bytes(b"gleich")

    s = _lauf(ziel)

    assert s.stat["verschoben"] == 1
    assert (ziel / "Duplicates" / "a_1.jpg").exists(), "Duplikat landet im Ziel"
    assert not (quelle / "Duplicates").exists(), "in der Quelle wird nichts angelegt"
    assert (quelle / "a_1.jpg").exists(), "Quelle bleibt unberuehrt"


def test_duplicates_ordner_wird_nicht_erneut_bearbeitet(tmp_path):
    ziel = tmp_path / "ziel"
    (ziel / "Duplicates").mkdir(parents=True)
    (ziel / "a.jpg").write_bytes(b"gleich")
    (ziel / "Duplicates" / "a_1.jpg").write_bytes(b"gleich")

    s = _lauf(ziel)

    assert s.stat["gesamt"] == 1, "nur a.jpg wird gesammelt"
    assert s.stat["verschoben"] == 0
    assert (ziel / "Duplicates" / "a_1.jpg").exists()
