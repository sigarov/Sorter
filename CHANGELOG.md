# Änderungshistorie

Hier werden alle Änderungen am Projekt fortlaufend dokumentiert – mit Datum
und laufender Nummer, damit jederzeit nachvollziehbar ist, was wann und warum
geändert wurde.

**Format:** `V-NNN` = laufende Nummer. Die Uebersicht ist aufsteigend sortiert
(V-001 oben, neuester Eintrag unten). Auch die Einzelabschnitte sind aufsteigend
sortiert (V-001 oben, neuester Eintrag unten).

---

## Übersicht

| Nr. | Datum | Kurzbeschreibung | Dateien |
|---|---|---|---|
| V-001–V-007 | 2026-10-07 | Grundüberarbeitung (Punkte 4–7 der Analyse) | `sorter.py`, `dedup_sorter.py`, `main.py`, `gui.py`, `translations.py`, `help_texts.py`, `README.md`, `requirements*.txt`, `pyproject.toml`, `conftest.py`, `tests/` (neu) |
| V-008 | 2026-10-07 | Hinweis „keine _1, _2 anlegen“ | `translations.py`, `help_texts.py` |
| V-009 | 2026-10-07 | Option „endgültig löschen“ entfernt | `gui.py`, `dedup_sorter.py`, `translations.py`, `help_texts.py`, `README.md` |
| V-010 | 2026-10-07 | Sorter überspringt `_Duplikate` | `config.py`, `sorter.py`, `dedup_sorter.py` |
| V-011 | 2026-10-07 | `geloescht_liste` → `verschoben_liste` | `dedup_sorter.py` |
| V-012 | 2026-10-07 | Force-Beschreibung präzisiert + Hilfetext | `translations.py`, `help_texts.py` |
| V-013 | 2026-10-07 | Umlaut `gelöscht=` im Fortschrittstext | `dedup_sorter.py` |
| V-014 | 2026-10-07 | Option „Vorhandene Dateien überspringen“ neu formuliert | `translations.py` |
| V-015 | 2026-10-07 | Hilfetext „Umbenennen ohne Basisdatei“ | `translations.py`, `help_texts.py` |
| V-016 | 2026-10-07 | Einzelne `_1`-Datei wird in Basisnamen umbenannt | `dedup_sorter.py`, `translations.py`, `help_texts.py`, `README.md`, `tests/test_dedup.py` |
| V-017 | 2026-10-07 | Nummerierung auf `V-` umgestellt, Tabellen eingefügt, Uebersicht aufsteigend | `CHANGELOG.md` |
| V-018 | 2026-10-07 | Einzelabschnitte aufsteigend sortiert | `CHANGELOG.md` |
| V-019 | 2026-10-07 | Uebersicht an Abschnitte angeglichen, V-017-Text praezisiert | `CHANGELOG.md` |
| V-020 | 2026-10-08 | Block A: echte Bugs behoben | `.gitignore`, `config.py`, `pyproject.toml`, `requirements.txt`, `README.md`, `gui.py`, `sorter.py`, `tests/test_utils.py` |
| V-021 | 2026-10-08 | Block B: toter Code und ungenutzte Keys entfernt | `dedup_sorter.py`, `translations.py`, `tests/test_i18n.py` |
| V-022 | 2026-10-08 | Block C: Log/Report/Fortschritt uebersetzt | `sorter.py`, `dedup_sorter.py`, `gui.py`, `translations.py`, `tests/` |
| V-023 | 2026-10-08 | Block D: Speicherplatzpruefung, Log-Begrenzung, gezieltes Logging | `utils.py`, `sorter.py`, `gui.py`, `main.py`, `translations.py`, `tests/` |
| V-024 | 2026-10-08 | Block E: gemeinsame Basisklasse, App-Verzeichnis, config/translations gegliedert | `worker_base.py` (neu), `sorter.py`, `dedup_sorter.py`, `config.py`, `main.py`, `gui.py`, `translations.py`, `tests/test_scan.py` |
| V-025 | 2026-10-08 | Block E: Tooling (ruff, LICENSE, CI), doppelte Keys entfernt | `pyproject.toml`, `requirements-dev.txt`, `LICENSE`, `.github/workflows/ci.yml`, `translations.py`, `tests/` |
| V-026 | 2026-10-08 | Block F: `lang_pfad` korrigiert, Hilfe-Titel uebersetzt | `utils.py`, `gui.py`, `translations.py` |
| V-027 | 2026-10-08 | Unterordner `Sort` → `Sorted` (Quelle = Ziel) | `config.py`, `gui.py`, `README.md`, `tests/test_gui_ziel.py` |
| V-028 | 2026-10-08 | „Wählen" öffnet im zuletzt gewählten Ordner (Schlüssel-Fehler) | `gui.py`, `tests/test_gui_paths.py` |
| V-029 | 2026-10-08 | `pip install ".[exif]"` repariert; `.tmp`-Reste verfälschen den Index nicht mehr | `pyproject.toml`, `sorter.py`, `tests/test_sorter_run.py` |
| V-030 | 2026-10-08 | Ordnernamen im Ziel immer englisch (`Pictures`, `Videos`, `_No_Date`) | `config.py`, `sorter.py`, `gui.py`, `help_texts.py`, `translations.py`, `README.md`, `tests/` |
| V-031 | 2026-10-08 | Vorschau: alle Quellen + effektives Ziel; Bugfix Quelle = Ziel | `gui.py`, `tests/test_gui_start.py` |
| V-032 | 2026-10-08 | Force-Modus mit Bestätigungsdialog | `gui.py`, `translations.py`, `tests/test_gui_start.py` |
| V-033 | 2026-10-08 | Fenstergeometrie wird vor dem Setzen geprüft | `gui.py`, `tests/test_gui_start.py` |
| V-034 | 2026-10-08 | Speicher-Leck: drei Schreib-nur-Listen im DedupSorter entfernt | `dedup_sorter.py` |
| V-035 | 2026-10-08 | `ruff format` eingeführt, CI erweitert, Doku/Installation geklärt | `pyproject.toml`, `.github/workflows/ci.yml`, `README.md`, `requirements.txt`, alle `.py` |
| V-036 | 2026-10-08 | Duplikat-Ordner `_Duplikate` → `Duplicates` (+ Abwärtskompatibilität) | `config.py`, `translations.py`, `worker_base.py`, `dedup_sorter.py`, `gui.py`, `README.md`, `tests/` |
| V-037 | 2026-10-08 | Dedup läuft nur im Zielordner und erst nach dem ersten Sortierlauf | `dedup_sorter.py`, `sorter.py`, `gui.py`, `help_texts.py`, `translations.py`, `conftest.py`, `README.md`, `tests/` |
| V-038 | 2026-10-13 | Build-Skripte für Windows-EXE und Linux-AppImage | `.gitignore`, `build_windows.bat` (neu), `build_linux_appimage.sh` (neu) |
| V-039 | 2026-10-18 | Trockenlauf-Cache beschleunigt den folgenden Echtlauf | `sorter.py`, `translations.py`, `README.md`, `tests/test_index_cache.py` (neu) |
| V-040 | 2026-10-18 | Übersetzungen nach Sprachen aufgeteilt (`i18n/`) | `translations.py`, `i18n/` (neu), `pyproject.toml`, `tests/test_i18n.py` |
| V-041 | 2026-10-18 | Sprachdateien in das Package `translations/` verschoben | `translations/` (neu), `translations.py` (entfernt), `pyproject.toml`, `tests/test_i18n.py`, `README.md` |
| V-042 | 2026-10-18 | GUI-Initialisierung in `_build_*`-Methoden zerlegt, Altlasten entfernt | `gui.py`, `CHANGELOG.md` |
| V-043 | 2026-10-18 | GUI weiter aufgeteilt, Smoke-Test, Coverage/Linux-CI, Dedup nur noch ueber den Tab | `gui.py`, `translations/*.py`, `tests/test_gui_smoke.py` (neu), `requirements-dev.txt`, `pyproject.toml`, `.github/workflows/ci.yml`, `README.md`, `CHANGELOG.md` |

---

## 2026-10-07

### V-001 bis V-007 – Grundüberarbeitung (Punkte 4–7 der Analyse)

**V-001 – Fortschrittscode entdoppelt**
Die dreifach vorhandenen Fortschrittsblöcke in `sorter.py` und der Block in
`dedup_sorter.py` wurden in je eine Methode `_melde_fortschritt()` ausgelagert.
*Dateien:* `sorter.py`, `dedup_sorter.py`

**V-002 – Stille Fehler sichtbar gemacht**
`except Exception: pass` schreibt jetzt per `log.debug(..., exc_info=True)` in
das Log (Ziel-Index nicht lesbar, Index-Eintrag fehlgeschlagen).
*Dateien:* `sorter.py`, `dedup_sorter.py`

**V-003 – Zentrales Logging**
`main.py` richtet eine Logdatei unter `~/.medien_sortierer/app.log` ein.
*Dateien:* `main.py`

**V-004 – Projekt-Tooling**
`requirements.txt`, `requirements-dev.txt`, `pyproject.toml` (mit
pytest-Konfiguration), `README.md`, `conftest.py` sowie Tests unter `tests/`
(`test_utils.py`, `test_naming.py`, `test_i18n.py`).
*Dateien:* neu angelegt

**V-005 – GUI/UX**
DPI-Bewusstsein unter Windows, plattformübergreifendes `_open_path()`
(Windows/macOS/Linux), Abbruch-Bestätigung in `stoppen()`, `?`-Button für den
Log-Bereich.
*Dateien:* `gui.py`

**V-006 – Internationalisierung abgesichert**
Hilfe-Sektion `log`, neue Keys `hint_log`, `confirm_cancel_title`,
`confirm_cancel_msg`; Test, dass alle Sprachen identische Keys haben und
`gui.py` nur existierende Keys verwendet.
*Dateien:* `translations.py`, `help_texts.py`, `tests/`

**V-007 – Hinweis „keine _1, _2 anlegen"**
Neuer Key `hint_skip_existing` in der Allgemein-Hilfe.
*Dateien:* `translations.py`, `help_texts.py`

---

### V-008 – Hinweis zur Option „keine _1, _2 anlegen"

Ergänzung in der Allgemein-Hilfe, dass die Option für den Fall gedacht ist, dass
zwei Quellen unterschiedliche Bilder mit gleichem Namen enthalten.

**Dateien:** `translations.py`, `help_texts.py`

---

### V-009 – Option „endgültig löschen" entfernt

Die Bereinigen-Ansicht bietet nur noch **„nach `_Duplikate` verschieben"** an.
Grund: Duplikate sollen erst visuell geprüft werden, bevor etwas gelöscht wird –
das endgültige Löschen umging genau diese Prüfung und war nicht rückgängig zu
machen.

- Aktionsauswahl (Label + zwei Radio-Buttons) aus `gui.py` entfernt.
- `dedup_action`-Variable und der `move_to_dupes`-Parameter entfernt.
- `_do_delete()` und der Lösch-Zweig in `dedup_sorter.py` entfernt.
- Report nennt nur noch verschobene/behaltene/kopierte Dateien.
- 11 überflüssige Übersetzungs-Keys entfernt, Texte auf „verschieben"
  umgestellt.

**Dateien:** `gui.py`, `dedup_sorter.py`, `translations.py`, `help_texts.py`,
`README.md`

---

### V-010 – Sorter überspringt den Ordner `_Duplikate`

Damit einmal aussortierte Dateien nicht beim nächsten Sortieren wieder ins Ziel
wandern, wird `_Duplikate` jetzt auch vom Sorter ignoriert.

- Neue zentrale Konstante `DUPES_FOLDER = "_Duplikate"` in `config.py`.
- `sorter.py` schließt den Ordner in `sammle_dateien()` aus.
- `dedup_sorter.py` nutzt die gemeinsame Konstante statt eines eigenen Literals.

**Dateien:** `config.py`, `sorter.py`, `dedup_sorter.py`

---

### V-011 – Liste umbenannt: `geloescht_liste` → `verschoben_liste`

Die Liste sammelt die nach `_Duplikate` verschobenen Dateien – der alte Name
stammte noch aus der Zeit, als endgültig gelöscht werden konnte.

**Dateien:** `dedup_sorter.py`

---

### V-012 – Beschreibung der Zusatzregel (Force) präzisiert

Der Text „… mit anderem Inhalt" war irreführend (klang nach „andere Motive").
Neu: „… mit **abweichendem** Inhalt" plus ein erklärender Hilfetext
`hint_dedup_force`, der die beiden Ursprünge beschreibt:

1. Dieselben Bilder, zu verschiedenen Zeiten gesichert.
2. Bilder aus zwei verschiedenen Kameras mit zufällig gleichem Namen.

**Dateien:** `translations.py`, `help_texts.py`

---

### V-013 – Deutsche Umlaute im Fortschrittstext

In der Fortschrittszeile des Dedup-Laufs stand `geloescht=` statt `gelöscht=`.

**Dateien:** `dedup_sorter.py`

---

### V-014 – Beschreibung der Option „Vorhandene Dateien überspringen"

Der Hilfetext `hint_skip_existing` wurde neu formuliert: Die Option ist für
**gleiche Sicherungen mit unterschiedlichen Zeitstempeln** gedacht und spart
dadurch Zeit bei der Duplikat-Sortierung und der manuellen Kontrolle.

**Dateien:** `translations.py`

---

### V-015 – Hilfetext „Umbenennen ohne Basisdatei"

Neuer Hilfetext `hint_dedup_rename` in allen 7 Sprachen, eingebunden in die
Dedup-Hilfe (`?`-Button im Tab „Bereinigen").

> Umbenennen ohne Basisdatei: Fehlt die Basisdatei (z. B. IMG.jpg), wird die
> Datei mit der kleinsten Nummer – auch eine einzelne _1-Datei – in den
> Basisnamen umbenannt (IMG_1.jpg -> IMG.jpg). Die Datei bleibt im Quellordner
> und wird nicht nach '_Duplikate' verschoben.

**Dateien:** `translations.py`, `help_texts.py`

---

### V-016 – Einzelne `_1`-Datei wird umbenannt

Bisher wurden nur Gruppen mit mindestens zwei Dateien bearbeitet. Eine
alleinstehende `IMG_1.jpg` (ohne `IMG.jpg` und ohne `IMG_2.jpg`) blieb
unangetastet. Jetzt wird auch sie in den Basisnamen umbenannt.

- Neue Methode `_relevante_gruppen()` in `dedup_sorter.py`: nimmt zusätzlich
  Gruppen mit genau einer Datei auf, wenn diese eine Nummer (`_1`, `_2`, ...)
  trägt.
- Eine einzelne Datei **ohne** Nummer (`IMG.jpg`) bleibt weiterhin unberührt.
- Bei der Einzeldatei wird nur umbenannt, keine Kopie nach `_Duplikate` gelegt.
- Klassendocstring und `README.md` ergänzt.

| Gruppe | Ergebnis |
|---|---|
| `IMG.jpg` allein | unangetastet – keine Umbenennung nötig |
| `IMG_1.jpg` allein | wird zu `IMG.jpg` umbenannt |
| `IMG.jpg` + `IMG_1.jpg` | bearbeitet (wie bisher) |

**Dateien:** `dedup_sorter.py`, `translations.py`, `help_texts.py`, `README.md`,
`tests/test_dedup.py` (neu)

---

### V-017 – Nummerierung auf `V-` umgestellt, Tabellen eingefügt

Die laufende Nummer wurde auf das einheitliche Format `V-NNN` umgestellt. Zusätzlich
enthält die Datei jetzt Tabellen: eine Übersichtstabelle aller Einträge am
Anfang, Verhaltenstabellen bei den Dedup-Einträgen und eine Testverteilung im
Verifikationsabschnitt. Die Uebersicht ist aufsteigend sortiert (V-001 oben,
neuester Eintrag unten).

**Dateien:** `CHANGELOG.md`

---

### V-018 – Einzelabschnitte aufsteigend sortiert

Die Einzelabschnitte unter ‚2026-10-07‘ sind jetzt ebenfalls aufsteigend
sortiert (V-001 oben, V-018 unten) – vorher stand der neueste Eintrag zuerst.
Damit ist die gesamte Datei einheitlich von alt nach neu lesbar.

**Dateien:** `CHANGELOG.md`



---

### V-019 – Uebersicht an die Abschnitte angeglichen

Die Übersichtstabelle und die Einzelabschnitte waren nicht deckungsgleich: V-001
bis V-007 standen in der Übersicht einzeln, in den Abschnitten aber als ein
gemeinsamer Block. Jetzt gibt es in der Übersicht ebenfalls einen Eintrag
‚V-001–V-007‘. Zusätzlich nennt der V-017-Abschnitt nun die aufsteigende
Sortierung der Übersicht, passend zur Übersichtszeile.

**Dateien:** `CHANGELOG.md`

---

## 2026-10-08

### V-020 – Block A: echte Bugs behoben

Ausgangspunkt war eine Analyse der Codebasis; Block A umfasst die sechs echten
Fehler. Es wurde sonst nichts umgestellt.

- **`.gitignore`:** Zeile 1 begann mit `*#`, war damit kein Kommentar, sondern
  ein (wirkungsloses) Glob-Muster – korrigiert zu `#`.
- **`gui.py`:** Im Log-Poll wurden bei einem `error`-Eintrag Start/Stop
  zurückgesetzt, **obwohl der Worker noch lief** – so konnte ein zweiter Lauf
  parallel gestartet werden. Die Buttons werden jetzt nur noch bei `finished`
  zurückgesetzt.
- **`sorter.py`:** Kopieren lief über `shutil.copy2` (nicht atomar, keine
  Groessenpruefung). Jetzt wird der vorhandene, bisher ungenutzte Helfer
  `kopiere_verifiziert()` verwendet: Schreiben in `.tmp`, Groessenvergleich,
  dann `os.replace`. Ein Abbruch hinterlaesst keine halbe Datei im Ziel.
- **`sorter.py`:** Das Aufnahmedatum wurde inline nur aus EXIF und Dateiname
  bestimmt; der vorhandene Helfer `ermittle_datum()` (EXIF → Video-Metadaten via
  `ffprobe` → Dateiname) war ungenutzt. **Video-Metadaten wurden beim Sortieren
  also ignoriert** – jetzt nicht mehr.
- **`pyproject.toml` / `requirements.txt` / `README.md`:** `Pillow` war in
  `pyproject.toml` eine harte Abhaengigkeit, laut README aber optional. Jetzt
  ueberall optional (Extra `exif`).
- **`config.py`:** Nur `ImportError` wurde gefangen – ein vorhandenes, aber
  defektes Pillow liess die App beim Start abstuerzen. Das Laden steckt jetzt in
  `_lade_pillow()` (siehe V-024).

**Dateien:** `.gitignore`, `config.py`, `pyproject.toml`, `requirements.txt`,
`README.md`, `gui.py`, `sorter.py`, `tests/test_utils.py`

---

### V-021 – Block B: toter Code und ungenutzte Keys entfernt

- `dedup_sorter.py`: ungenutzte Imports `Path` und `_NullWriter` sowie der nie
  verwendete Logger `log` (inkl. `import logging`) entfernt.
- `dedup_sorter.py`: `stat["geloescht"]` wurde nie erhoeht – Key und Anzeige
  entfernt (Altlast der in V-009 entfernten Loesch-Option).
- `translations.py`: die drei ungenutzten Keys `lbl_mode`, `msg_dedup_info` und
  `report_dedup_ready` aus allen 7 Sprachen entfernt.
- `tests/test_i18n.py`: **neuer Reverse-Test** `test_keine_unbenutzten_keys()` –
  sammelt alle String-Literale der Projektdateien (AST) und schlaegt Alarm, wenn
  ein uebersetzter Key nirgends verwendet wird. Bisher gab es nur die
  Gegenrichtung (Key fehlt).

**Dateien:** `dedup_sorter.py`, `translations.py`, `tests/test_i18n.py`

---

### V-022 – Block C: Log, Report und Fortschritt uebersetzt

Bisher schrieben Sorter und Dedup-Sorter ihre Log- und Reportzeilen **fest auf
Deutsch**, obwohl ein Uebersetzungssystem vorhanden ist. Nutzer mit EN/RU/FR/ES/
PL/TR bekamen deutsche Ausgaben.

- `sorter.py`: Fortschrittszeile, `DUP:`, `SKIP (exists)`, `ERROR (read)`,
  `ERROR:`, Start-/Ende-Header, Trockenlauf-Banner, Report-Kopf und -Summe in
  der Logdatei sowie „Duplikate pro Ordner“ laufen jetzt ueber `self.T(...)`.
- `dedup_sorter.py`: Dedup-Fortschritt und der Kopf des Trockenlauf-Logs.
- `gui.py`: Die Fortschrittstexte wurden ueber ein **inline-Woerterbuch im Code**
  gebaut (7 Sprachen mitten in der Methode) – jetzt ueber die Keys
  `lbl_index_progress` / `lbl_sort_progress`.
- `gui.py`: Der Fertig-Dialog zeigt die **uebersetzten Report-Zeilen** aus dem
  Log statt roher `stat`-Schluessel; gibt es keine (z. B. bei Abbruch), werden
  Fehler/Warnungen gezeigt.
- Fenstertitel ueber neues `window_title` uebersetzbar (Markenname bleibt bei EN).
- **Neue Keys (7 Sprachen):** `log_progress`, `log_dedup_progress`,
  `log_dup_entry`, `log_skip_exists`, `log_error_read`, `log_error_file`,
  `log_start_header`, `log_end_header`, `log_report_file`,
  `lbl_index_progress`, `lbl_sort_progress`, `window_title`.

**Dateien:** `sorter.py`, `dedup_sorter.py`, `gui.py`, `translations.py`

---

### V-023 – Block D: Robustheit und Ressourcen

- **Speicherplatzpruefung:** Neue Helfer `lesbare_groesse()` und `freier_platz()`
  in `utils.py`; `Sorter._platz_reicht()` summiert die Quelldateien und bricht
  **vor dem ersten Kopiervorgang** mit uebersetzter Meldung ab (`log_not_enough_space`).
  Ist der freie Platz nicht ermittelbar (z. B. Netzlaufwerk), wird nicht
  abgebrochen; im Trockenlauf greift die Pruefung nicht.
- **Log begrenzt:** `_log_lines` ist jetzt eine `deque(maxlen=50000)`,
  zusaetzlich kuerzt `_trim_log_text()` das Text-Widget (`MAX_LOG_ZEILEN`).
  Vorher wuchs der Puffer bei langen Laeufen unbegrenzt.
- **Vorschau-Scan:** `_confirm_preview()` ueberspringt jetzt `_Duplikate` und den
  Zielordner und nutzt den neuen Groessen-Formatierer.
- **Gezieltes Logging:** `gui.py` hat einen Logger; die zuvor stillen
  `except Exception: pass` in `_load_settings`, `_save_settings`, `_open_path`,
  `_show_finish_dialog`, `_log_clear`, `_trim_log_text` und im Vorschau-Scan
  schreiben jetzt per `log.debug(..., exc_info=True)` in die App-Logdatei.
- **`main.py`:** ruft `logging.shutdown()` im `finally` – letzte Logzeilen gehen
  beim Beenden nicht mehr verloren.
- **Neuer Key:** `log_not_enough_space` (7 Sprachen).

**Dateien:** `utils.py`, `sorter.py`, `gui.py`, `main.py`, `translations.py`,
`tests/test_sorter_run.py` (neu), `tests/test_gui_log.py` (neu)

---

### V-024 – Block E: gemeinsame Basis, App-Verzeichnis, Gliederung

- **`worker_base.py` (neu):** `MediaWorker` als gemeinsame Basis fuer `Sorter`
  und `DedupSorter`. Beide hatten `T()`, `melde()`, `melde_finished()`,
  `_melde_fortschritt()` und – fast identisch – `sammle_dateien()` dupliziert.
  Jetzt liegen Quellen/Filter, Log-Queue, Fortschritt und die Scan-Logik
  (inkl. `_Duplikate`- und Zielordner-Ausschluss) einmal in der Basis; die
  Unterklassen liefern nur noch ihre Eigenheiten (`_ist_zielordner()`,
  Trockenlauf-Log, Statistiken).
- **App-Verzeichnis zentral:** `APP_DIR` und `app_dir()` in `config.py`; `main.py`
  und `gui.py` hatten `~/.medien_sortierer` jeweils selbst zusammengebaut.
- **`config.py` gegliedert** in optionale Abhaengigkeiten (mit `_lade_pillow()`),
  App-Verzeichnis, Dateitypen, Ordner/Dateinamen und GUI-Optionen.
- **`translations.py`:** uneinheitliche Einrueckung bereinigt (14 ueber-eingerueckte
  Zeilen auf 8 Leerzeichen) und ein Test ergaenzt, der das Format kuenftig
  erzwingt.
- **Tests ergaenzt:** `tests/test_scan.py` fuer die gemeinsame Scan-Logik
  (Medienerkennung, `_Duplikate`-, Ziel- und `SKIP_NAMES`-Ausschluss,
  Ordnerfilter).

**Dateien:** `worker_base.py` (neu), `sorter.py`, `dedup_sorter.py`, `config.py`,
`main.py`, `gui.py`, `translations.py`, `tests/test_scan.py` (neu),
`tests/test_i18n.py`

---

### V-025 – Block E: Tooling, Lizenz, CI und doppelte Keys

- **Ruff als Linter** eingerichtet (`[tool.ruff]` in `pyproject.toml`, Regeln
  `E`, `F`, `W`, `I`, `B`; `E501` aus) und in `requirements-dev.txt` /
  Dev-Extra aufgenommen. Der Lauf ist sauber.
- **Ruff fand einen echten Bug:** In `translations.py` waren die Keys
  `log_drylogfile` und `report_dedup_remaining` in **jeder** Sprache doppelt
  vorhanden (14 Zeilen). Alle Duplikate waren wertgleich und wurden entfernt.
  Die bestehenden Tests pruefen nur Mengengleichheit der Keys, nicht auf
  Duplikate – deshalb war das unbemerkt geblieben.
- Weitere Ruff-Funde behoben: unsortierte Imports, ungenutzter Import
  `VIDEO_EXT` in `sorter.py`, f-String ohne Platzhalter, ungenutzte
  Schleifenvariablen (`B007`) und drei Anweisungen mit Semikolon in `gui.py`.
- **`LICENSE`** (MIT) ergaenzt; `pyproject.toml` nennt `license`, `readme` und
  die Dev-Abhaengigkeiten.
- **CI** unter `.github/workflows/ci.yml`: Windows-Runner, Python 3.9 und 3.12,
  `ruff check .` und `pytest`.
- **Tests ergaenzt:** `hash_datei()`, `lang_pfad()` (Tests/test_utils.py) sowie
  `tests/test_dedup_run.py` fuer einen echten Dedup-Durchlauf (verschieben,
  abweichenden Inhalt behalten, Trockenlauf aendert nichts).

**Dateien:** `pyproject.toml`, `requirements-dev.txt`, `LICENSE`,
`.github/workflows/ci.yml`, `translations.py`, `sorter.py`, `gui.py`,
`tests/test_utils.py`, `tests/test_dedup_run.py` (neu)

---

### V-026 – Block F: Kleinigkeiten

- **`utils.lang_pfad()`:** machte unter Windows **jeden** Pfad absolut und
  veraenderte damit kurze/relative Pfade. Jetzt werden kurze Pfade unveraendert
  zurueckgegeben (wie `os.fspath`); nur lange Pfade bekommen den Prefix. Die
  Grenze 240 ist kommentiert: sie laesst Luft bis zur 260er-Grenze, weil der
  Kopierer voruebergehend `.tmp` anhaengt.
- **`gui._zeige_hilfe()`:** Der Fallback-Titel war hartkodiert `"Hilfe"`; jetzt
  ueber den neuen Key `dlg_help_title` (7 Sprachen).

**Dateien:** `utils.py`, `gui.py`, `translations.py`

---

### V-027 – Unterordner heisst jetzt `Sorted`

Sind Quelle und Ziel identisch, leitet die App in einen Unterordner um, damit die
unsortierten Quelldateien nicht in den Zielindex geraten. Dieser Ordner hiess
`Sort` und heisst jetzt einheitlich **`Sorted`** – fest, in allen Sprachen gleich
(kein Uebersetzungs-Key, anders als `folder_pictures` usw.).

- `config.py`: `SORT_UNTERORDNER = "Sorted"`.
- `gui.py`: Docstring von `_effektives_ziel()` auf `Sorted` angepasst.
- `README.md`: Hinweis auf `Sorted` aktualisiert.
- `tests/test_scan.py`: Testordner mit umbenannt.
- **Neuer Test** `tests/test_gui_ziel.py`: sichert die Umleitung selbst und den
  Ordnernamen ab (Konstante, Quelle 1 = Ziel, Quelle 2 = Ziel, Normalfall).

> Hinweis: Bereits vorhandene `Sort`-Ordner aus frueheren Laeufen werden **nicht**
> automatisch umbenannt.

**Dateien:** `config.py`, `gui.py`, `README.md`, `tests/test_scan.py`,
`tests/test_gui_ziel.py` (neu)

---

### V-028 – „Wählen" öffnet im zuletzt gewählten Ordner

Beim Klick auf **Wählen** öffnete der Ordner-Dialog immer am Standardort, statt dort,
wo zuletzt gewählt wurde. Ursache war ein **Schlüssel-Mismatch**: Die Buttons gaben
`"source1"`, `"source2"` und `"target"` mit, gespeichert und geladen wurden die Pfade
aber unter `"q1"`, `"q2"`, `"ziel"`. `waehle()` suchte dadurch immer ins Leere und
konnte den gemerkten Pfad nie als `initialdir` verwenden. Der Fehler steckte schon im
Commit `5f34ca1` – er fiel nur nicht auf, weil das Feld ohnehin leer startet.

- Neue Methoden `_pfad_felder()` (einzige Quelle der Wahrheit fuer die drei Pfadfelder)
  und `_feld_key()`.
- `waehle(var)` bestimmt den Schluessel jetzt selbst; die Buttons werden ohne
  Schluessel aufgerufen – so koennen die Namen nicht mehr auseinanderlaufen.
- `_remember_paths()` und `_load_settings()` nutzen ebenfalls `_pfad_felder()`.
- Verhalten sonst unveraendert: Die Eingabefelder bleiben beim Start leer, gemerkt
  wird nur ein tatsaechlich gewaehlter oder eingetragener Pfad.
- **Neue Tests** `tests/test_gui_paths.py`: gemerkter Ordner wird als `initialdir`
  benutzt, Rueckfall auf den Feldinhalt, kein `initialdir` ohne bekannten Ordner,
  Speichern unter dem Feld-Schluessel, Laden aus `settings.json`.

> Hinweis: `settings.json` liegt weiterhin unter `~/.medien_sortierer/` und wird
> beim Beenden geschrieben. Alte Schluessel (`source1` usw.) waren wirkungslos und
> werden nicht mehr benutzt.

**Dateien:** `gui.py`, `tests/test_gui_paths.py` (neu)

---

### V-029 – Nachanalyse: Paketinstallation und `.tmp`-Reste

Beim erneuten Durchsehen des Projekts fielen zwei weitere Fehler auf.

**1. `pip install ".[exif]"` war unbrauchbar.** Die README verweist fuer die
optionale EXIF-Unterstuetzung darauf, aber der Aufruf brach ab: Ohne
`[build-system]`/Paketangaben scheitert die automatische Erkennung im
Flat-Layout („Multiple top-level modules discovered"). Es fehlte ausserdem ein
Build-Backend.

- `[build-system]` mit `setuptools>=61` ergaenzt.
- `[tool.setuptools] py-modules = [...]` listet die neun Projektmodule explizit
  auf; damit ist die Installation (und das Extra `exif`) nutzbar.
- Geprueft mit `pip install --dry-run --no-deps ".[exif]"` → Metadaten-Erzeugung
  laeuft durch.

**2. Liegen gebliebene `.tmp`-Dateien im Ziel verfaelschten den Index.**
`kopiere_verifiziert()` schreibt erst nach `name.tmp` und benennt dann um. Bei
einem harten Abbruch (Stromausfall, Kill) bleibt so eine Datei liegen. Der
Ziel-Index (`_index.txt`-Aufbau) nahm sie mit auf – ihre Pruefsumme stand danach
in `known`. Eine **echte Quelldatei mit gleichem Inhalt wurde dadurch als
Duplikat erkannt und nie kopiert**. Die Datei fehlte dann im Ziel.

- `indexiere_ziel()` ueberspringt jetzt Dateien auf `.tmp`.
- Fremde `.tmp`-Dateien werden bewusst **nicht** geloescht (keine Datenvernichtung).
- Neuer Test in `tests/test_sorter_run.py`: eine `.tmp`-Datei im Ziel blockiert
  keine Quelle mehr und bleibt selbst unangetastet.

**Dateien:** `pyproject.toml`, `sorter.py`, `tests/test_sorter_run.py`

---

### V-030 – Ordnernamen im Ziel immer englisch

Wunsch: Die Ordnerstruktur im Ziel soll **unabhaengig von der GUI-Sprache** immer
englisch sein. Bisher kamen die Namen aus den Uebersetzungen – und
`folder_pictures` war in **allen** Sprachen ausser Englisch auf `"Bilder"`
gesetzt, russische/franzoesische/spanische/polnische/tuerkische Nutzer bekamen
also deutsche Ordnernamen.

- Neue feste Konstanten in `config.py`: `FOLDER_PICTURES = "Pictures"`,
  `FOLDER_VIDEOS = "Videos"`, `FOLDER_NO_DATE = "_No_Date"` (wie schon
  `SORT_UNTERORDNER = "Sorted"` bewusst nicht uebersetzt).
- `sorter.py` nutzt die Konstanten statt `lang.get("folder_*")`.
- `gui.py` zeigt im Hinweistext den festen Namen `_No_Date`.
- Die drei `folder_*`-Keys aus allen 7 Sprachen entfernt (21 Zeilen) – die
  Reverse-Pruefung haette sie sonst als unbenutzt gemeldet.
- **Neuer Test** `test_ordnernamen_sind_immer_englisch` (parametrisiert ueber
  alle 7 Sprachen) laeuft einen echten Sortiervorgang und prueft
  `Pictures/2020`, `Videos/2020` und `_No_Date/Pictures`.

**Dateien:** `config.py`, `sorter.py`, `gui.py`, `help_texts.py`,
`translations.py`, `README.md`, `tests/test_sorter_run.py`

---

### V-031 – Vorschau zeigt alle Quellen und das effektive Ziel

- Die Vorschau nannte als Quelle nur **Quelle 1** – wer ausschliesslich
  Quelle 2 nutzte, sah `-`. Jetzt werden alle gewaehlten Quellen aufgelistet.
- Das Ziel wird als **effektives** Ziel angezeigt (bei Quelle = Ziel also
  `…\Sorted`), passend zu dem, was der Lauf wirklich tut.
- **Bugfix:** Der Vorschau-Scan ueberspringt den Zielordner – bei
  **Quelle = Ziel** war das der Quellordner selbst, also wurden **0 Dateien**
  gezaehlt und der Start ohne Rueckfrage durchgewunken. Jetzt wird nur das
  effektive Ziel (`<Ziel>/Sorted`) ausgelassen.
- **Neue Tests** in `tests/test_gui_start.py`: beide Quellen erscheinen,
  `Sorted` erscheint bei Quelle = Ziel, `_Duplikate` wird nicht mitgezaehlt.

**Dateien:** `gui.py`, `tests/test_gui_start.py` (neu)

---

### V-032 – Force-Modus verlangt eine Bestaetigung

Die erweiterte Regel verschiebt auch `_1`, `_2`-Dateien mit **abweichendem**
Inhalt nach `_Duplikate` – ohne den Inhalt zu vergleichen. Das passierte bisher
ohne jede Rueckfrage. Jetzt fragt die App vor dem Start nach.

- Neue Keys `confirm_force_title` / `confirm_force_msg` (7 Sprachen).
- Die Startpruefungen wurden aus `start()` in die neue Methode
  `_bestaetige_start()` gezogen (Rueckgabe `False` = nicht starten). Dadurch ist
  das Verhalten testbar.
- **Neue Tests:** Nachfrage im Force-Modus, Abbruch bricht ab, ohne Force wird
  nicht gefragt, fehlende Quelle/Ziel warnt.

**Dateien:** `gui.py`, `translations.py`, `tests/test_gui_start.py`

---

### V-033 – Fenstergeometrie wird geprueft

Die gespeicherte Geometrie wurde ungeprueft gesetzt. Nach einem Monitorwechsel
konnte das Fenster ausserhalb des sichtbaren Bereichs landen – die App war dann
unsichtbar.

- Neue Methoden `_geometry_zerlegen()` und `_geometrie_passt()`; nur passende
  Geometrien werden uebernommen. Negative Offsets (am rechten/unteren Rand
  verankert) gelten als sichtbar.
- **Neue Tests** fuer das Zerlegen und die Bildschirmpruefung.

**Dateien:** `gui.py`, `tests/test_gui_start.py`

---

### V-034 – Speicher-Leck im DedupSorter beseitigt

`behalten_liste`, `verschoben_liste` und `diff_liste` wurden bei jedem
behandelten Duplikat gefuellt, aber **nirgends gelesen** (ausgewertet werden nur
`stat`, `error_liste` und `pro_ordner`). Bei sehr grossen Laeufen hielten sie
unbegrenzt Pfade im Speicher. Die drei Listen und ihre Schreibzugriffe sind
entfernt; die Statistiken bleiben unveraendert.

**Dateien:** `dedup_sorter.py`

---

### V-035 – Formatierung, CI und Doku-Feinschliff

- **`ruff format`** eingefuehrt (`line-ending = "auto"`, damit CRLF erhalten
  bleibt). 15 Dateien wurden einmalig formatiert; die CI prueft es kuenftig mit
  `ruff format --check .`.
- **Hilfetext-Bugfix:** Der `?-Button` „Allgemein" zeigte das rohe
  `{nodate}` – `get_help()` ersetzt den Platzhalter jetzt durch `_No_Date`.
  Neuer Test `test_get_help_hat_keine_rohen_platzhalter`.
- **README:** Installationswege geklaert (es gibt **keine** Pflicht-Abhaengigkeit
  mehr; `Pillow` optional per `pip install Pillow` oder `.[exif]`), Hinweis auf
  die festen englischen Ordnernamen, Formatpruefung dokumentiert.
- **`requirements.txt`** als bewusst leere Platzhalterdatei kommentiert.

**Dateien:** `pyproject.toml`, `.github/workflows/ci.yml`, `README.md`,
`requirements.txt`, `help_texts.py`, `tests/test_i18n.py`, alle `.py`

---

### V-036 – Duplikat-Ordner heisst jetzt `Duplicates`

Der Ordner fuer aussortierte Duplikate hiess `_Duplikate` – der letzte deutsche
Ordnername im Programm (und der einzige mit Unterstrich).

- `DUPES_FOLDER = "Duplicates"` in `config.py`.
- Alle Texte in allen 7 Sprachen angepasst (`translations.py`: 67 Stellen
  `_Duplikate` → `Duplicates`), ebenso `README.md` und die Docstrings.
- **Abwaertskompatibilitaet:** Der alte Name wird weiterhin erkannt und beim
  Einsammeln uebersprungen (`DUPES_FOLDER_ALTE` + Helfer `ist_dupes_ordner()`,
  genutzt in `worker_base.py` und `gui.py`). Ohne das wuerden die bereits
  aussortierten Dateien aus einem alten `_Duplikate`-Ordner beim naechsten
  Sortieren **wieder ins Ziel kopiert** werden.
- **Neue Tests** in `tests/test_scan.py`: `ist_dupes_ordner()` erkennt den neuen
  **und** den alten Namen, und ein alter `_Duplikate`-Ordner wird beim Sammeln
  uebersprungen.

> Hinweis: Ein bereits vorhandener `_Duplikate`-Ordner wird **nicht** automatisch
> umbenannt – neue Duplikate landen in `Duplicates`.

**Dateien:** `config.py`, `translations.py`, `worker_base.py`, `dedup_sorter.py`,
`gui.py`, `README.md`, `tests/test_scan.py`

---

### V-037 – Dedup laeuft nur noch im Zielordner und erst nach dem Sortieren

Bisher arbeitete die Bereinigung auf den **Quellordnern**; im Dedup-Tab war das
Ziel ausgegraut. Sinnvoll ist sie aber im **Ziel**, weil dort beim Sortieren die
`_1`, `_2`-Dateien entstehen. Umgesetzt in vier Teilen.

**1. Worker laeuft auf dem Ziel**
- `DedupSorter(ziel, trockenlauf, force, lang, log_queue, stop_event)` statt
  zweier Quellen mit Filtern; `_quelle_fuer_pfad()` entfaellt,
  `_dupes_dst()` wird zu `<Ziel>/Duplicates/<rel>` (Spiegelung wie bisher).
- Das Trockenlauf-Log liegt jetzt im Ziel.
- Neue Meldung `log_dedup_ziel` mit dem Pfad (ersetzt `log_dedup_start`).

**2. Ziel-Index ueberspringt `Duplicates`**
- `indexiere_ziel()` laesst den Duplikat-Ordner aus. Ohne das wuerde der
  aussortierte Inhalt als „schon vorhanden" gelten und spaetere Kopien blockieren.

**3. GUI: nur das Ziel ist aktiv**
- Im Dedup-Modus sind Quellfelder, Filterfelder und die beiden
  „Waehlen"-Buttons gesperrt; Ziel-Feld und Ziel-Button sind aktiv (vorher
  umgekehrt). Dafuer gibt es jetzt Widget-Referenzen (`q1_entry`, `filter1_entry`, …).
- `lbl_target_dedup` heisst jetzt „Zielordner zum Bereinigen"; die Keys
  `lbl_source1_dedup` und `lbl_source2_dedup` sind entfallen.
- `_bestaetige_start()` verlangt im Dedup-Modus ein **Ziel** (nicht mehr Quellen).

**4. Freigabe erst nach dem ersten Sortierlauf**
- Merkmal ist die `_index.txt`, die der Sorter am Ende jedes echten Laufs
  schreibt (`_ziel_mit_index()`, `_dedup_freigabe()`, `_dedup_ziel()`).
- Der Dedup-Haken ist gesperrt und der Tab heisst „Bereinigen (gesperrt)"
  (`mode_dedup_locked`). Ein Klick auf den Tab zeigt `hint_dedup_locked` und
  springt zurueck zum Sortieren. (Tk kann einen Tab nicht ausgrauen **und** einen
  Klick melden – daher gesperrte Beschriftung plus Hinweis statt echter Sperre.)
- Geprueft wird beim Start, nach dem Zielwechsel (Button oder Tippen im Feld),
  nach jedem Lauf und beim Sprachwechsel.
- Wurde mit Quelle = Ziel sortiert, liegt der Index in `<Ziel>/Sorted`; dieser
  Unterordner wird automatisch als Dedup-Ziel vorgeschlagen.

**Testinfrastruktur:** `conftest.py` ersetzt jetzt automatisch **alle**
messagebox-Dialoge. Vorher konnte ein Test an einem echten, blockierenden
Dialog haengen bleiben.

**Dateien:** `dedup_sorter.py`, `sorter.py`, `gui.py`, `help_texts.py`,
`translations.py`, `conftest.py`, `README.md`, `tests/test_dedup_run.py`,
`tests/test_sorter_run.py`, `tests/test_scan.py`, `tests/test_gui_start.py`

---

### V-038 – Build-Skripte fuer Windows-EXE und Linux-AppImage

Bisher gab es keinen reproduzierbaren Weg, aus dem Projekt eine
weitergebbare Anwendung zu bauen. Jetzt liegen zwei Skripte bei, die
PyInstaller interaktiv aufrufen und die Umgebung vorab pruefen. Beide fragen
Eingabedatei (Standard `main.py`) und App-Namen ab, zeigen eine Zusammenfassung
und lassen sich vor dem Start abbrechen.

**1. `build_windows.bat` – Windows-EXE**
- Sucht Python bevorzugt ueber den `py`-Launcher, sonst `python`; bricht mit
  einer Installationsanleitung ab, wenn keins gefunden wird.
- Installiert PyInstaller nur, wenn es fehlt.
- Baut `--onefile --windowed` nach `dist\<Name>.exe`; ein angehaengtes `.exe`
  im eingegebenen Namen wird entfernt.

**2. `build_linux_appimage.sh` – Linux-AppImage**
- Laeuft nur unter Linux und bricht auf Windows/macOS mit Hinweis auf WSL2/VM
  ab.
- Prueft `python3`, `wget`, `file` und `tkinter` vorab, damit Tk spaeter nicht
  in der AppImage fehlt.
- Baut in einer eigenen `.build-venv` mit `--onedir --windowed`, erzeugt
  `AppDir` inklusive `AppRun` und `.desktop`-Datei und uebernimmt `icon.png`
  (sonst wird ein schlichtes Platzhalter-Icon erzeugt).
- Holt `appimagetool` nur bei Bedarf und weicht bei fehlendem FUSE auf
  `--appimage-extract-and-run` aus; Ergebnis ist `<Name>-x86_64.AppImage`.

**3. `.gitignore` ergaenzt**
- PyInstaller-/AppImage-Artefakte werden ignoriert: `*.spec`, `AppDir/`,
  `.build-venv/`, `appimagetool-*.AppImage`, `*.AppImage`. Die Build-Skripte
  selbst bleiben versioniert.

**Geprueft:** `bash -n build_linux_appimage.sh` ohne Fehler; Abbruchpfad und
tkinter-Schutzpfad getestet; Ignorier-Regeln greifen (eine beim ersten Build
entstandene `Sortierer.spec` bleibt bewusst untracked).

**Dateien:** `.gitignore`, `build_windows.bat` (neu),
`build_linux_appimage.sh` (neu)

---

### V-039 – Trockenlauf-Cache beschleunigt den folgenden Echtlauf

Bisher hat der Trockenlauf den Zielordner zwar vollstaendig gehasht, das
Ergebnis aber weggeworfen. Der Echtlauf begann danach wieder bei null und las
alle Zieldateien erneut – derselbe Zyklus also zweimal. Jetzt uebernimmt der
Echtlauf die Hashes des Trockenlaufs.

**1. Separater Cache statt `_index.txt`**
- Der Trockenlauf schreibt am Ende von `indexiere_ziel()` seine
  `index_entries` in `~/.medien_sortierer/index-cache/<hash>.txt`
  (eine Datei pro Zielordner, Schluessel aus dem normalisierten Zielpfad).
- `_index.txt` bleibt unangetastet: Sie ist der Freigabe-Marker fuer den
  Dedup-Tab und entsteht weiterhin nur im echten Lauf.
- Der Cache hat denselben Zeilentyp wie der Index, zusaetzlich einen
  Versionskopf und den Zielpfad. Geschrieben wird atomar ueber eine
  PID-eindeutige `.tmp`-Datei und `os.replace`.

**2. Echtlauf nutzt beide Quellen**
- `indexiere_ziel()` laedt `_index.txt` **und** den Trockenlauf-Cache und
  fuehrt sie zusammen. Bei gleichem Pfad gewinnt `_index.txt`; der Cache
  ergaenzt Dateien, die seit dem letzten echten Lauf dazugekommen sind.
- Die Gueltigkeit prueft weiterhin jede Datei einzeln ueber Groesse und
  mtime_ns. Geaenderte, neue oder geloeschte Dateien werden wie bisher
  behandelt; veraltete Eintraege werden einfach neu gehasht.
- Nach einem erfolgreichen `speichere_index()` wird der Cache geloescht –
  `_index.txt` ist dann vollstaendiger. Schlaegt das Speichern fehl, bleibt
  der Cache als Rueckfallebene erhalten (`speichere_index()` liefert dafuer
  jetzt einen Bool).

**3. Meldungen und Tests**
- Vier neue Uebersetzungs-Keys in allen 7 Sprachen: Cache geladen,
  gespeichert, Lese- und Schreibfehler.
- `tests/test_index_cache.py` prueft: Trockenlauf legt Cache, aber keinen
  Index an; Echtlauf hasht Zieldateien nicht erneut und entfernt den Cache;
  Duplikaterkennung funktioniert trotz Cache; geaenderte Zieldatei wird neu
  gehasht; kaputter Cache wird ignoriert; Cache ist pro Ziel getrennt.

**Geprueft:** `python -m pytest` 99 Tests, alle gruen; `ruff check .` und
`ruff format --check .` ohne Befund.

**Dateien:** `sorter.py`, `translations.py`, `README.md`,
`tests/test_index_cache.py` (neu)

---

### V-040 – Uebersetzungen nach Sprachen aufgeteilt

`translations.py` war mit 977 Zeilen und 136 Keys in 7 Sprachen unhandlich.
Die Datei ist jetzt nur noch ein Aggregator; jede Sprache liegt in einer
eigenen Datei unter `i18n/`.

**1. Aufteilung**
- `i18n/en.py`, `de.py`, `ru.py`, `fr.py`, `es.py`, `pl.py`, `tr.py` mit je
  140 Zeilen; jedes Modul exportiert ein Dict (`EN`, `DE`, ...).
- `translations.py` importiert die sieben Dicts und baut `TRANSLATIONS`
  unveraendert in der bisherigen Reihenfolge zusammen.
- Die Werte wurden maschinell aus dem alten Modul uebernommen und vor dem
  Schreiben auf Gleichheit geprueft (alle 952 Eintraege identisch).

**2. Packaging**
- `pyproject.toml`: `i18n` als Package eingetragen. Ein Wheel-Build enthaelt
  `translations.py` und alle sieben Sprachmodule.
- PyInstaller/EXE/AppImage: keine Aenderung noetig, die Module werden ueber
  die Imports automatisch gebunden (keine Datendateien, kein `--add-data`).

**3. Tests**
- `test_i18n.py` prueft die Einrueckung jetzt in allen `i18n/*.py`
  (Schluessel mit 4 Leerzeichen) und dass jedes Sprachmodul ein Dict
  exportiert.
- Unveraendert: gleiche Key-Menge in allen Sprachen, keine unbenutzten Keys,
  Help-Texte.

**Geprueft:** `python -m pytest` 100 Tests gruen; `ruff check .` und
`ruff format --check .` ohne Befund; Wheel-Build enthaelt `i18n/*.py`.

**Dateien:** `translations.py`, `i18n/` (neu), `pyproject.toml`,
`tests/test_i18n.py`

> Hinweis: Der Zwischenschritt mit `i18n/` wurde direkt anschliessend in
> V-041 in das Package `translations/` ueberfuehrt.

---

### V-041 – Sprachdateien in das Package `translations/`

V-040 hatte die Sprachen in ein separates `i18n/`-Package gelegt und
`translations.py` als Aggregator stehen lassen. Jetzt ist auch der Aggregator
ein Package: `translations/__init__.py`. Damit gibt es nur noch einen
Übersetzungsordner.

- `i18n/en.py` … `tr.py` → `translations/en.py` … `tr.py`; die Inhalte
  wurden unveraendert uebernommen.
- `translations/__init__.py` importiert mit relativen Imports
  (`from .de import DE`, …) und baut `TRANSLATIONS` in der bisherigen
  Reihenfolge zusammen.
- `translations.py` ist entfallen.
- `pyproject.toml`: `translations` ist jetzt ein Package; der Eintrag in
  `py-modules` wurde entfernt.
- Tests: Einrueckungspruefung und Modul-Import laufen ueber
  `translations/*.py`.
- Der oeffentliche Import bleibt unveraendert:
  `from translations import TRANSLATIONS`.

**Geprueft:** Der Inhalt ist vor und nach dem Verschieben identisch (alle
952 Eintraege); `python -m pytest` 100 Tests gruen; `ruff check .` und
`ruff format --check .` ohne Befund; das Wheel enthaelt
`translations/__init__.py` und alle sieben Sprachmodule.

**Dateien:** `translations/` (neu), `translations.py` (entfernt),
`pyproject.toml`, `tests/test_i18n.py`, `README.md`

---

### V-042 – GUI-Initialisierung in `_build_*`-Methoden zerlegt

Der 346-Zeilen-`__init__` von `App` hat Variablen, Fenster, Widgets und
Startlogik vermischt. Jetzt ist er eine kurze Abfolge; der UI-Aufbau steckt in
`_build_*`-Methoden.

- `_init_vars()`, `_init_window()` und `_build_ui()` als klare Phasen.
- `_build_ui()` ruft `_build_language_bar()`, `_build_sources_column()`,
  `_build_options_column()`, `_build_separator()`, `_build_log_panel()` und
  `_build_status_bar()` auf.
- Quelle 1 und 2 teilen sich jetzt `_build_source_block()`; vorher war der
  Block fast identisch dupliziert.
- Zielblock, Start/Stop-Buttons und Fortschrittsbalken sind eigene Methoden.
- Die Widget-Namen (`q1_entry`, `btn_w1`, `filter1_entry`, `txt`, `nb`, …)
  bleiben unveraendert, damit `_apply_language`, `_on_dedup_toggle` und die
  GUI-Tests weiter funktionieren.

**Altlasten-Audit (Changelog):**
- `_on_mode_change()` und `modus_var` waren nur noch geschrieben, nie gelesen –
  entfernt (Rest der frueheren Modus-Radio-Buttons).
- In den aktuellen Abschnitten des Changelogs standen noch `_Duplikate`-
  Referenzen; sie heissen jetzt `Duplicates`.
- Die doppelten, veralteten `_Duplikate`-Bullets unter „Offene Punkte" sind
  entfernt.
- `_Duplikate` bleibt nur dort absichtlich erhalten, wo die
  Abwaertskompatibilitaet es braucht (`DUPES_FOLDER_ALTE`, Test in
  `test_scan.py`).

**Geprueft:** 100 Tests gruen; `ruff check .` und `ruff format --check .` ohne
Befund.

**Dateien:** `gui.py`, `CHANGELOG.md`

---

### V-043 – GUI-Feinschliff, Smoke-Test und einheitlicher Dedup-Schalter

V-042 hatte den UI-Aufbau in `_build_*`-Methoden zerlegt. V-043 zieht die noch
grossen Methoden nach, sichert den echten GUI-Aufbau mit einem Test ab und
beseitigt den doppelten Dedup-Schalter.

**1. GUI weiter aufgeteilt**
- `_build_options_column()` ruft jetzt `_build_general_group()`,
  `_build_mode_tabs()`, `_build_dedup_group()` und `_build_naming_group()` auf.
- `_apply_language()` ist in `_apply_language_groups()`,
  `_apply_language_header()`, `_apply_language_sources()`,
  `_apply_language_options()`, `_apply_language_tabs()` und
  `_apply_language_log()` zerlegt.
- `_update_source_labels()` ist die einzige Stelle fuer Quell-/Zieltexte und
  wird von `_apply_language_sources()` und `_on_dedup_toggle()` genutzt.
- `_set_widget_state()` ersetzt die wiederholten `try/except tk.TclError`-
  Schleifen; die Ein-Element-Schleife fuer die Force-Checkbox ist entfallen.
- Die `hasattr`-Absicherungen in `_apply_language()` sind entfernt, weil die
  Methode erst nach `_build_ui()` laeuft.

**2. Dedup nur noch ueber den Tab**
- Die Checkbox `chk_dedup` ist entfernt; der Tab „Bereinigen" ist der einzige
  Modusschalter. `self.dedup` bleibt als interner Zustand erhalten.
- Der Uebersetzungs-Key `chk_dedup` ist aus allen sieben Sprachdateien
  entfernt; `chk_dedup_force` bleibt unveraendert.
- `_aktualisiere_dedup_freigabe()` muss dadurch kein Widget mehr sperren und
  setzt nur noch Modus und Tab-Titel.

**3. Tests und CI**
- `tests/test_gui_smoke.py` (neu) baut die echte `App` auf und prueft Widgets,
  Sprachwechsel, Dedup-Sperre und das Sperren der Quellen im Dedup-Modus.
  Ohne Display wird der Test uebersprungen.
- `pytest-cov` ist in `requirements-dev.txt`; Coverage-Konfiguration liegt in
  `pyproject.toml`.
- CI: Windows-Job misst Coverage; neuer Linux-Job (Python 3.12) fuehrt Lint und
  Tests unter `xvfb-run` aus.

**Geprueft:** 105 Tests gruen; `ruff check .` und `ruff format --check .` ohne
Befund; GUI-Smoke-Test baut die Oberflaeche erfolgreich auf.

**Dateien:** `gui.py`, `translations/*.py`, `tests/test_gui_smoke.py` (neu),
`requirements-dev.txt`, `pyproject.toml`, `.github/workflows/ci.yml`,
`README.md`, `CHANGELOG.md`

---

## Verhalten im Detail

### Umbenennen und Verschieben

Ausgangslage: `IMG_1.jpg` und `IMG_2.jpg` liegen im Quellordner, `IMG.jpg` fehlt.

| Ort | Datei | Aktion |
|---|---|---|
| Quellordner | `IMG.jpg` | durch **Umbenennen** aus `IMG_1.jpg` – bleibt liegen |
| `Duplicates` | `IMG_2.jpg` | **verschoben** |
| `Duplicates` | `IMG.jpg` | **Kopie** des Keepers (einmal pro Gruppe) |

### Einzelne Datei ohne Basisdatei

Ausgangslage: nur `IMG_1.jpg` liegt im Quellordner.

| Ort | Datei | Aktion |
|---|---|---|
| Quellordner | `IMG.jpg` | durch **Umbenennen** aus `IMG_1.jpg` |
| `Duplicates` | – | keine Kopie (keine Duplikat-Schleife) |

---

## Verifikation (Stand 2026-10-07)

| Prüfung | Ergebnis |
|---|---|
| `python -m py_compile` (alle Module) | ohne Fehler |
| `python -m pytest` | 22 Tests, alle grün |
| Übersetzungen | 122 Keys in allen 7 Sprachen, keine Abweichungen |

**Testverteilung**

| Testdatei | Tests |
|---|---|
| `test_i18n.py` | 3 |
| `test_naming.py` | 7 |
| `test_translation_usage.py` | 1 |
| `test_utils.py` | 7 |
| `test_dedup.py` | 4 |
| **gesamt** | **22** |

---

## Verifikation (Stand 2026-10-08)

| Prüfung | Ergebnis |
|---|---|
| `python -m py_compile` (alle Module) | ohne Fehler |
| `ruff check .` | All checks passed |
| `ruff format --check .` | alle Dateien formatiert |
| `python -m pytest` | 92 Tests, alle grün |
| Übersetzungen | 132 Keys in allen 7 Sprachen, keine Abweichungen, keine Duplikate |
| Ordnernamen im Ziel | immer englisch (`Pictures`, `Videos`, `_No_Date`), für alle 7 Sprachen geprüft |
| Dedup-Ablauf | Ende-zu-Ende: sortieren → Freigabe → bereinigen nur im Ziel (Quelle unberührt) |
| Echter Trockenlauf von `Sorter` und `DedupSorter` in DE/EN/RU/TR | ohne Fehler, Ausgabe in der jeweiligen Sprache |
| `pip install --dry-run ".[exif]"` | Metadaten-Erzeugung läuft durch |

**Testverteilung**

| Testdatei | Tests |
|---|---|
| `test_gui_start.py` | 22 |
| `test_utils.py` | 16 |
| `test_sorter_run.py` | 12 |
| `test_scan.py` | 7 |
| `test_naming.py` | 7 |
| `test_gui_paths.py` | 6 |
| `test_i18n.py` | 6 |
| `test_dedup_run.py` | 5 |
| `test_dedup.py` | 4 |
| `test_gui_ziel.py` | 4 |
| `test_gui_log.py` | 2 |
| `test_translation_usage.py` | 1 |
| **gesamt** | **78** |

---

## Verifikation (Stand 2026-10-18)

| Prüfung | Ergebnis |
|---|---|
| `python -m pytest` | 105 Tests, alle grün |
| `ruff check .` | All checks passed |
| `ruff format --check .` | alle Dateien formatiert |
| GUI-Smoke-Test | echte `App` aufgebaut, alle Widgets vorhanden |
| CI | Windows (3.9/3.12) mit Coverage, Linux (3.12) mit `xvfb-run` |

**Testverteilung**

| Testdatei | Tests |
|---|---|
| `test_gui_start.py` | 22 |
| `test_utils.py` | 16 |
| `test_sorter_run.py` | 12 |
| `test_scan.py` | 7 |
| `test_naming.py` | 7 |
| `test_i18n.py` | 7 |
| `test_index_cache.py` | 7 |
| `test_gui_paths.py` | 6 |
| `test_dedup_run.py` | 5 |
| `test_dedup.py` | 4 |
| `test_gui_ziel.py` | 4 |
| `test_gui_smoke.py` | 5 |
| `test_gui_log.py` | 2 |
| `test_translation_usage.py` | 1 |
| **gesamt** | **105** |

---

## Offene Punkte (noch nicht umgesetzt)

Aus der ursprünglichen Liste sind inzwischen erledigt:

- ~~Integritätsprüfung nach dem Kopieren~~ → umgesetzt (V-020,
  `kopiere_verifiziert()` vergleicht die Dateigroesse)
- ~~Rollback / atomares Kopieren (`.tmp` + `os.replace`)~~ → umgesetzt (V-020)
- ~~Dry-Run: Duplikate innerhalb der Quelle werden nicht als Duplikat erkannt~~
  → Duplikate werden auch im Trockenlauf erkannt (Eintrag in `known`)
- ~~`exif_datum()` schließt das Bild nicht~~ → nutzt `with Image.open(...)`
- ~~Warnung/Bestätigung für den Force-Modus~~ → umgesetzt (V-032)
- ~~Doppelter Schalter für den Dedup-Modus~~ → umgesetzt (V-043): der Tab
  „Bereinigen" ist der einzige Modusschalter, die Checkbox ist entfernt

Weiterhin offen:

- **Papierkorb statt endgültigem Löschen** – bewusst nicht umgesetzt: es wird
  grundsätzlich nichts gelöscht, Duplikate wandern nach `Duplicates` (V-009).
- **Endgültiges Löschen von `Duplicates`** – bleibt bewusst manuell.
- **Tk-Tabs lassen sich nicht ausgrauen *und* Klicks melden.** Deshalb zeigt der
  gesperrte Tab „Bereinigen (gesperrt)" und erklaert beim Klick den Grund,
  statt wirklich deaktiviert zu sein.
- **Log-/Reporttexte der Worker** sind inzwischen übersetzt; die Dateinamen
  darin (`_log.txt`, `_index.txt`) bleiben fest.
