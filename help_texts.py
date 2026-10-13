"""Hilfetexte für die ?-Buttons (abgeleitet aus den Übersetzungen)."""

from config import FOLDER_NO_DATE
from translations import TRANSLATIONS

# Welche Übersetzungs-Schlüssel gehören zu welchem Hilfe-Abschnitt
HELP_SECTIONS = {
    "general": (
        "chk_dryrun",
        "chk_skip_existing",
        "hint_skip_existing",
        "hint_text",
    ),
    "dedup": (
        "hint_dedup_first_run",
        "hint_dedup_locked",
        "hint_dedup_move",
        "hint_dedup_rename",
        "chk_dedup_force",
        "hint_dedup_force",
    ),
    "naming": (
        "naming_original",
        "naming_datum_name",
        "naming_datum_zeit_name",
        "naming_iso_name",
        "naming_nummer",
        "naming_datum_nummer",
    ),
    "log": ("hint_log",),
}


def get_help(lang_code, section):
    """Liefert den Hilfetext für einen Abschnitt in der gewählten Sprache.

    Der Platzhalter ``{nodate}`` wird durch den festen englischen Ordnernamen
    ersetzt – sonst stünde im Hilfetext das rohe ``{nodate}``."""
    lang = TRANSLATIONS.get(lang_code) or TRANSLATIONS.get("de", {})
    keys = HELP_SECTIONS.get(section, ())
    parts = [lang[k] for k in keys if k in lang]
    return "\n\n".join(parts).replace("{nodate}", FOLDER_NO_DATE)
