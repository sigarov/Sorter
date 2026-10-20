"""Handbuch (Bedienungsanleitung) je Sprache.

Die Handbuchtexte liegen bewusst ausserhalb von ``TRANSLATIONS``: Sie sind
lang, nicht als UI-Label gedacht und wuerden die Uebersetzungs-Tests (gleiche
Keys in allen Sprachen) unuebersichtlich machen.

Jedes Handbuch ist ein Dict mit ``title`` und ``sections``. Eine Section ist
ein Dict mit ``id``, ``title`` und ``text``. Die ``id`` ist sprachunabhaengig
und bleibt in allen Uebersetzungen gleich.
"""

from .de import DE
from .en import EN
from .es import ES
from .fr import FR
from .pl import PL
from .ru import RU
from .tr import TR

# Unbekannte Sprachen fallen auf Deutsch zurueck.
MANUALS = {"de": DE, "en": EN, "ru": RU, "fr": FR, "es": ES, "pl": PL, "tr": TR}

FALLBACK = "de"


def get_manual(lang_code):
    """Liefert das Handbuch der Sprache (unbekannt -> Deutsch)."""
    return MANUALS.get(lang_code) or MANUALS[FALLBACK]


def get_sections(lang_code):
    """Kapitel des Handbuchs als Liste von Dicts (id, title, text)."""
    return get_manual(lang_code)["sections"]


def get_section(lang_code, section_id):
    """Kapitel per ID; eine unbekannte ID liefert das erste Kapitel."""
    sections = get_sections(lang_code)
    for section in sections:
        if section["id"] == section_id:
            return section
    return sections[0]
