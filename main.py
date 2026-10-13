"""Einstiegspunkt des Sortierers."""

import logging
import os

from config import app_dir
from gui import App


def _setup_logging():
    """Schreibt Log-Meldungen in die Datei im App-Verzeichnis.

    Dadurch sind zuvor stille Fehler (z. B. nicht lesbare Index-Eintraege)
    nachvollziehbar, ohne die GUI zu veraendern."""
    try:
        logging.basicConfig(
            filename=os.path.join(app_dir(), "app.log"),
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            encoding="utf-8",
        )
    except Exception:
        pass


if __name__ == "__main__":
    _setup_logging()
    try:
        App().mainloop()
    finally:
        logging.shutdown()
