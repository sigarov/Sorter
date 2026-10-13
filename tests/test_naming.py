"""Tests fuer Dateinamen- und Pfadbildung des Sorters."""

from datetime import datetime

from sorter import Sorter


def _sorter(naming="original", granularitaet="year"):
    """Erzeugt ein Sorter-Objekt ohne Thread-Initialisierung."""
    s = Sorter.__new__(Sorter)
    s.naming = naming
    s.granularitaet = granularitaet
    s.nummer_counter = {}
    return s


def test_neuer_dateiname_original():
    s = _sorter(naming="original")
    assert s.neuer_dateiname("foto.JPG", datetime(2020, 1, 2), None) == "foto.jpg"


def test_neuer_dateiname_datum_name():
    s = _sorter(naming="datum_name")
    assert s.neuer_dateiname("foto.JPG", datetime(2020, 1, 2), None) == "20200102_foto.jpg"


def test_neuer_dateiname_datum_zeit_name():
    s = _sorter(naming="datum_zeit_name")
    assert (
        s.neuer_dateiname("foto.JPG", datetime(2020, 1, 2, 3, 4, 5), None)
        == "20200102_030405_foto.jpg"
    )


def test_neuer_dateiname_iso_name():
    s = _sorter(naming="iso_name")
    assert s.neuer_dateiname("foto.JPG", datetime(2020, 1, 2), None) == "2020-01-02_foto.jpg"


def test_neuer_dateiname_nummer(tmp_path):
    s = _sorter(naming="nummer")
    assert s.neuer_dateiname("foto.JPG", datetime(2020, 1, 2), tmp_path) == "00001.jpg"


def test_neuer_dateiname_ohne_datum():
    s = _sorter(naming="datum_name")
    assert s.neuer_dateiname("foto.JPG", None, None) == "foto.jpg"


def test_datum_pfad_teile():
    s = _sorter(granularitaet="year")
    assert s.datum_pfad_teile(datetime(2020, 5, 6)) == ["2020"]
    s.granularitaet = "month"
    assert s.datum_pfad_teile(datetime(2020, 5, 6)) == ["2020", "05"]
    s.granularitaet = "day"
    assert s.datum_pfad_teile(datetime(2020, 5, 6)) == ["2020", "05", "06"]
