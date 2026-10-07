"""Hilfetexte für die ?-Buttons (abgeleitet aus den Übersetzungen)."""

from translations import TRANSLATIONS

# Welche Übersetzungs-Schlüssel gehören zu welchem Hilfe-Abschnitt
HELP_SECTIONS = {
    "general": (
        "chk_dryrun",
        "chk_skip_existing",
        "hint_text",
    ),
    "dedup": (
        "hint_dedup_first_run",
        "lbl_dedup_hint",
        "hint_dedup_move",
        "hint_dedup_delete",
        "chk_dedup_force",
        "chk_move_to_dupes",
    ),
    "naming": (
        "naming_original",
        "naming_datum_name",
        "naming_datum_zeit_name",
        "naming_iso_name",
        "naming_nummer",
        "naming_datum_nummer",
    ),
}


def get_help(lang_code, section):
    """Liefert den Hilfetext für einen Abschnitt in der gewählten Sprache."""
    lang = TRANSLATIONS.get(lang_code) or TRANSLATIONS.get("de", {})
    keys = HELP_SECTIONS.get(section, ())
    parts = [lang[k] for k in keys if k in lang]
    return "\n\n".join(parts)
