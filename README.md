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
- **Trockenlauf:** simuliert alle Aktionen, ohne Dateien zu veraendern.
- **Mehrsprachig:** Englisch, Deutsch, Russisch, Franzoesisch, Spanisch,
  Polnisch, Tuerkisch.

## Start

```powershell
python main.py
```

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
ruff check .
ruff format --check .
```

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
- Vor dem Kopieren wird der freie Speicherplatz im Ziel geprueft; reicht er
  nicht, bricht der Lauf mit einer Meldung ab.
- Log und Einstellungen liegen im Ordner `~/.medien_sortierer`
  (`app.log`, `settings.json`).

## Lizenz

MIT, siehe `LICENSE`.