[![CI](https://github.com/sigarov/Sorter/actions/workflows/ci.yml/badge.svg)](https://github.com/sigarov/Sorter/actions/workflows/ci.yml)
# Medien-Sortierer

Tkinter-Tool zum Sortieren und Entdoppeln von Bildern und Videos.

## Funktionen

- **Sortieren:** kopiert Medien aus einer oder zwei Quellen in einen Zielordner,
  gruppiert nach Jahr/Monat/Tag (Granularitaet waehlbar) und optional getrennt
  nach Bilder/Videos.
- **Entdoppeln (im Zielordner):** laeuft **nur im Zielordner**, weil dort beim
  Sortieren die `NAME_1.jpg`, `NAME_2.jpg` usw. entstehen. Identische Dateien
  wandern in den Unterordner `Duplicates` (nichts wird geloescht). Dort kannst du
  in Ruhe pruefen, ob es echte Duplikate oder zwei verschiedene Bilder mit
  gleichem Namen sind, und den Ordner danach selbst aufraeumen. Der Ordner
  `Duplicates` wird beim Sortieren uebersprungen. Fehlt die Basisdatei, wird
  auch eine einzelne `NAME_1.jpg` in `NAME.jpg` umbenannt.
- **Trockenlauf:** simuliert alle Aktionen, ohne Dateien zu veraendern. Die
  dabei gelesenen Ziel-Hashes werden fuer den naechsten echten Lauf
  zwischengespeichert (`~/.medien_sortierer/index-cache`), damit der Zielordner
  nicht zweimal komplett gelesen wird. `_index.txt` entsteht weiterhin nur im
  echten Lauf.
- **Mehrsprachig:** Englisch, Deutsch, Russisch, Franzoesisch, Spanisch,
  Polnisch, Tuerkisch.
- **Handbuch:** Button „Hilfe“ oben rechts (oder `F1`) oeffnet eine
  Bedienungsanleitung mit zwoelf Kapiteln in der eingestellten Sprache. Die
  kleinen `?`-Buttons bleiben als Kurzhinweis pro Gruppe erhalten.

## Download & Starten

Du hast zwei Möglichkeiten, das Programm zu nutzen:

### Option 1: Fertige Programme (Empfohlen für Nutzer)
Lade dir die neueste Version direkt unter **[Releases](https://github.com/sigarov/Sorter/releases)** herunter.

* **Windows:** Lade die `.exe`-Datei herunter und starte sie mit einem Doppelklick.
* **Linux:** Lade die `.AppImage`-Datei herunter. Mache sie ausführbar (Rechtsklick -> Eigenschaften -> "Ausführbar" oder via Terminal mit `chmod +x dateiname.AppImage`) und starte sie per Doppelklick.

### Option 2: Aus dem Quellcode starten (Für Entwickler)
Wenn du Python installiert hast, kannst du das Programm direkt starten:

## Start

```powershell
python main.py
```

 ##Eigene Versionen erstellen (Build)

Im Repository liegen zwei Skripte, um eigene ausführbare Dateien zu erstellen:

· Windows (.exe): Führe build_windows.bat aus. Dies erstellt eine .exe-Datei im dist-Ordner.
· Linux (.AppImage): Führe build_linux_appimage.sh aus. Dies erstellt eine portable .AppImage-Datei. 
  (Hinweis: Unter Linux werden dafür Pakete wie python3-venv, binutils und das appimagetool benötigt, die das Skript größtenteils automatisch herunterlädt).

## Abhaengigkeiten

Es gibt **keine** Pflicht-Abhaengigkeiten – das Tool laeuft mit der
Standardbibliothek. `pip install -r requirements.txt` ist deshalb nur ein
Platzhalter.

Optional fuer EXIF-Aufnahmedaten (`Pillow`):

```powershell
pip install Pillow
# oder, wenn das Projekt installiert wird:
pip install ".[exif]"
```

Ohne Pillow wird kein EXIF-Datum gelesen; die Sortierung funktioniert
weiterhin, das Datum kommt dann aus Video-Metadaten (falls `ffprobe` im PATH
liegt) oder aus dem Dateinamen.

## Tests und Pruefung

```powershell
pip install -r requirements-dev.txt
python -m pytest
python -m pytest --cov --cov-report=term-missing
ruff check .
ruff format --check .
```

Der GUI-Smoke-Test baut die komplette Tk-Oberflaeche einmal auf. Unter Linux
braucht er ein Display, in CI laeuft er deshalb ueber `xvfb-run`.

Die Uebersetzungen liegen pro Sprache in `translations/` (`de.py`, `en.py`, ...).
`translations/__init__.py` buendelt sie nur noch zu `TRANSLATIONS`; Textaenderungen
gehoeren in die jeweilige Sprachdatei.

Das Handbuch liegt getrennt davon in `manual/` (`de.py`, `en.py`, `ru.py`,
`fr.py`, `es.py`, `pl.py`, `tr.py`). Es ist absichtlich nicht Teil von
`TRANSLATIONS`, weil die langen Kapitel sonst die Key-Paritaetstests aufblaehen.
Alle sieben Oberflaechensprachen sind uebersetzt; nur eine unbekannte Sprache
zeigt das deutsche Handbuch.

## Ablauf

1. **Sortieren** – Quellen waehlen, Ziel waehlen, starten. Im Ziel entsteht die
   Ordnerstruktur; bei Namensgleichheit kommen `_1`, `_2` usw. dazu.
2. **Entdoppeln** – Tab „Bereinigen" waehlen und **nur den Zielordner** angeben.
   Quellen und Filter sind dort gesperrt.

Der Tab „Bereinigen" ist **gesperrt**, solange im gewaehlten Ziel noch kein
Sortierlauf stattgefunden hat. Erkennungsmerkmal ist die `_index.txt`, die der
Sorter am Ende jedes echten Laufs schreibt. Ein Klick auf den gesperrten Tab
erklaert das und springt zurueck zum Sortieren.

## Hinweise

- Der Zielordner wird niemals mit-durchsucht, damit nichts doppelt sortiert wird.
- Sind Quelle und Ziel identisch, wird automatisch in den Unterordner `Sorted`
  umgeleitet. Die Bereinigung bietet diesen Unterordner dann automatisch an.
- **Die Ordnernamen im Ziel sind immer englisch** – unabhaengig von der
  eingestellten Sprache: `Pictures`, `Videos` und `_No_Date` (fuer Dateien ohne
  Datum), darunter Jahr/Monat/Tag. So bleibt die Struktur bei einem
  Sprachwechsel stabil.
- Im Zielordner beschleunigt ein Index (`_index.txt`) spaetere Laeufe erheblich.
  Er dient zugleich als Merkmal „hier wurde schon sortiert".
- Ein Trockenlauf schreibt **keine** `_index.txt` und gibt die Bereinigung nicht
  frei. Er legt nur einen Hash-Cache im App-Verzeichnis ab; der naechste echte
  Lauf nutzt ihn und entfernt ihn danach.
- Vor dem Kopieren wird der freie Speicherplatz im Ziel geprueft; reicht er
  nicht, bricht der Lauf mit einer Meldung ab.
- Log und Einstellungen liegen im Ordner `~/.medien_sortierer`
  (`app.log`, `settings.json`).

## Lizenz

MIT, siehe `LICENSE`.
