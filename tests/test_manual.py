"""Tests fuer das Handbuch (mehrsprachige Bedienungsanleitung)."""

from manual import MANUALS, get_manual, get_section, get_sections
from translations import TRANSLATIONS

# Reihenfolge und IDs sind sprachunabhaengig und gelten fuer jede Uebersetzung.
KAPITEL = [
    "intro",
    "start",
    "sort",
    "names",
    "structure",
    "filters",
    "dryrun",
    "dedup",
    "skip",
    "log",
    "settings",
    "keys",
]


def test_deutsch_hat_alle_kapitel_in_der_richtigen_reihenfolge():
    ids = [section["id"] for section in get_sections("de")]
    assert ids == KAPITEL


def test_kapitel_haben_titel_und_text():
    for code in MANUALS:
        for section in get_sections(code):
            ort = f"{code}/{section['id']}"
            assert section["title"].strip(), f"{ort}: Titel fehlt"
            assert section["text"].strip(), f"{ort}: Text fehlt"


def test_alle_sprachen_haben_gleiche_kapitel():
    basis = [section["id"] for section in get_sections("de")]
    for code in MANUALS:
        assert [section["id"] for section in get_sections(code)] == basis, f"Sprache {code}"


def test_handbuch_hat_einen_titel():
    for code in MANUALS:
        assert get_manual(code)["title"].strip(), f"{code}: Handbuch-Titel fehlt"


def test_keine_rohen_platzhalter():
    """Im Handbuch darf kein rohes {nodate} stehen (Ordnername ist fest)."""
    for code in MANUALS:
        for section in get_sections(code):
            assert "{nodate}" not in section["text"], f"{code}/{section['id']}"


def test_handbuch_deckt_alle_oberflaechensprachen_ab():
    assert set(MANUALS) == set(TRANSLATIONS)


def test_unbekannte_sprache_faellt_auf_deutsch_zurueck():
    assert get_manual("xx") is get_manual("de")


def test_unbekanntes_kapitel_liefert_das_erste():
    assert get_section("de", "gibt-es-nicht")["id"] == KAPITEL[0]


def test_kapitel_ist_per_id_auffindbar():
    for kapitel_id in KAPITEL:
        assert get_section("de", kapitel_id)["id"] == kapitel_id
