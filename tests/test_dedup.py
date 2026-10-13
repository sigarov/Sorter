"""Tests fuer die Gruppenauswahl des DedupSorter."""

from dedup_sorter import DedupSorter


def _gruppe(ordner, basis, ext, eintraege):
    return ((ordner, basis, ext), eintraege)


def test_normale_datei_ohne_suffix_wird_ignoriert():
    # Einzelne Datei ohne Nummer: kein Duplikat, keine Umbenennung.
    gruppen = dict([_gruppe("d", "img", ".jpg", [("d/img.jpg", 0)])])
    assert DedupSorter._relevante_gruppen(gruppen) == {}


def test_einzelne_datei_mit_nummer_wird_aufgenommen():
    # Einzelne _1-Datei ohne Basisdatei: soll umbenannt werden.
    gruppen = dict([_gruppe("d", "img", ".jpg", [("d/img_1.jpg", 1)])])
    relevante = DedupSorter._relevante_gruppen(gruppen)
    assert list(relevante) == [("d", "img", ".jpg")]


def test_mehrere_dateien_bleiben_kandidaten():
    gruppen = dict(
        [
            _gruppe("d", "a", ".jpg", [("d/a.jpg", 0), ("d/a_1.jpg", 1)]),
            _gruppe("d", "b", ".jpg", [("d/b_1.jpg", 1), ("d/b_2.jpg", 2)]),
        ]
    )
    relevante = DedupSorter._relevante_gruppen(gruppen)
    assert set(relevante) == {("d", "a", ".jpg"), ("d", "b", ".jpg")}


def test_gemischte_gruppen():
    gruppen = dict(
        [
            _gruppe("d", "allein", ".jpg", [("d/allein.jpg", 0)]),
            _gruppe("d", "eins", ".jpg", [("d/eins_3.jpg", 3)]),
            _gruppe("d", "paar", ".jpg", [("d/paar.jpg", 0), ("d/paar_1.jpg", 1)]),
        ]
    )
    relevante = DedupSorter._relevante_gruppen(gruppen)
    assert set(relevante) == {("d", "eins", ".jpg"), ("d", "paar", ".jpg")}
