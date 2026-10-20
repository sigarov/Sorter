"""Deutsches Handbuch - Mastervorlage fuer alle weiteren Sprachen."""

DE = {
    "title": "Bedienungsanleitung",
    "sections": [
        {
            "id": "intro",
            "title": "1. Was das Programm macht",
            "text": (
                "Der Medien-Sortierer ordnet Bilder und Videos in eine feste Ordnerstruktur "
                "und hilft anschliessend beim Aufraeumen von Namensdubletten.\n\n"
                "Du waehlst eine oder zwei Quellen (Ordner oder ganze Laufwerke) und einen "
                "Zielordner. Das Programm liest alle Bilder und Videos ein, ermittelt das "
                "Aufnahmedatum und kopiert jede Datei in den passenden Jahres-, Monats- und "
                "Tagesordner.\n\n"
                "Wichtig zu wissen:\n"
                "• Die Quellen werden nur gelesen, nie veraendert.\n"
                '• Es wird nichts geloescht. Duplikate wandern in den Ordner "Duplicates".\n'
                "• Die Ordnernamen im Ziel sind immer englisch (Pictures, Videos, _No_Date). "
                "So bleibt die Struktur bei einem Sprachwechsel stabil.\n"
                "• Die Oberflaeche gibt es in sieben Sprachen. Dieses Handbuch erscheint in "
                "der eingestellten Sprache, sobald es dafuer uebersetzt ist - bis dahin auf "
                "Deutsch."
            ),
        },
        {
            "id": "start",
            "title": "2. Erste Schritte",
            "text": (
                "1. Sprache oben links waehlen - die Anzeige wechselt sofort.\n"
                "2. Quelle 1 waehlen: Ordner oder Laufwerk. Optional Quelle 2 ergaenzen.\n"
                "3. Ziel waehlen: dorthin wird einsortiert.\n"
                "4. Optional den Trockenlauf aktivieren, um vorher zu simulieren.\n"
                '5. Auf "▶  Start" klicken (oder F5 druecken).\n\n'
                "Waehrend des Laufs zeigen zwei Fortschrittsbalken den Stand: erst die "
                'Indexierung des Ziels, dann das Sortieren. Mit "■  Stop" (oder Esc) brichst '
                "du ab; bereits kopierte Dateien bleiben erhalten.\n\n"
                'Der Tab "Bereinigen" ist erst nach einem echten Sortierlauf im gewaehlten '
                "Ziel freigeschaltet."
            ),
        },
        {
            "id": "sort",
            "title": "3. Sortieren und Ordnerstruktur",
            "text": (
                "Der Sortierlauf hat zwei Phasen:\n"
                "1. Der Zielordner wird indexiert. Dabei werden Groesse, Aenderungszeit und "
                "Pruefsumme (Hash) aller vorhandenen Dateien erfasst.\n"
                "2. Jede Quelldatei wird geprueft und in den Zielordner kopiert.\n\n"
                "So wird das Datum ermittelt (in dieser Reihenfolge):\n"
                "• EXIF-Aufnahmedatum des Bildes (benoetigt Pillow)\n"
                "• Metadaten des Videos (benoetigt ffprobe im PATH)\n"
                "• Datum aus dem Dateinamen, z. B. 2020-05-17, 20200517 oder 20200517_143025\n\n"
                "Das Datum aus dem Dateisystem wird bewusst nicht verwendet: Dateien ohne "
                "echte Zeitangabe sollen im Ordner _No_Date landen, statt mit dem Kopierdatum "
                "falsch einsortiert zu werden.\n\n"
                "Struktur im Ziel (Beispiel):\n"
                "• Pictures/2020/05/17/urlaub.jpg\n"
                "• Videos/2020/05/17/urlaub.mp4\n"
                "• _No_Date/Pictures/unbekannt.jpg\n\n"
                "Ist eine Zieldatei schon vorhanden und der Inhalt gleich, wird die Quelldatei "
                "uebersprungen. Bei gleichem Namen aber anderem Inhalt entstehen _1, _2 usw. "
                "Vor dem Kopieren prueft das Programm den freien Speicherplatz und vergleicht "
                "nach dem Kopieren die Dateigroesse."
            ),
        },
        {
            "id": "names",
            "title": "4. Dateinamen",
            "text": (
                "Sechs Varianten fuer neue Dateinamen (Beispiel: urlaub.jpg vom 17.05.2020, "
                "14:30:25):\n\n"
                "• Original: urlaub.jpg\n"
                "• Datum_Name: 20200517_urlaub.jpg\n"
                "• Datum_Zeit_Name: 20200517_143025_urlaub.jpg\n"
                "• Jahr-Monat-Tag_Name: 2020-05-17_urlaub.jpg\n"
                "• Nummer: 00001.jpg\n"
                "• Datum_Nummer: 20200517_0001.jpg\n\n"
                'Ohne Datum vergibt "Nummer" nur die laufende Nummer; bei allen anderen '
                "Varianten bleibt der urspruengliche Name. Die Endung wird immer klein "
                "geschrieben. Bei Namensgleichheit haengt das Programm _1, _2, ... an."
            ),
        },
        {
            "id": "structure",
            "title": "5. Struktur: getrennt oder zusammen",
            "text": (
                "Getrennt (Standard): Bilder und Videos liegen in eigenen Baeumen.\n"
                "  Pictures/2020/05/17/... und Videos/2020/05/17/...\n"
                "Zusammen: beide landen im selben Jahres-/Monats-/Tagesordner.\n"
                "  2020/05/17/...\n\n"
                "Granularitaet:\n"
                "• Jahr: 2020/\n"
                "• Monat: 2020/05/\n"
                "• Tag: 2020/05/17/\n\n"
                'Dateien ohne Datum landen in _No_Date - bei "Getrennt" zusaetzlich unter '
                "Pictures bzw. Videos. Dort listet _liste.txt alle betroffenen Dateien auf."
            ),
        },
        {
            "id": "filters",
            "title": "6. Ordner filtern",
            "text": (
                "Das Filterfeld grenzt ein, welche Unterordner der Quelle durchsucht werden.\n"
                "• Mehrere Begriffe mit Komma trennen: Fotos, Pictures, DCIM\n"
                "• Es zaehlen nur Ordnernamen, keine Dateiendungen.\n"
                "• Gross-/Kleinschreibung ist egal.\n"
                "• Ein Treffer gilt auch fuer alle Unterordner.\n"
                "• Leeres Feld = gesamte Quelle.\n\n"
                'Beispiel: In D:\\Backup liegen "Fotos", "Dokumente" und "Videos". Mit dem '
                'Filter "Fotos, Videos" werden nur diese beiden Ordner gelesen.\n\n'
                'Im Tab "Bereinigen" gibt es keinen Filter: dort wird immer der ganze '
                "Zielordner geprueft."
            ),
        },
        {
            "id": "dryrun",
            "title": "7. Trockenlauf und Index-Cache",
            "text": (
                "Der Trockenlauf zeigt, was passieren wuerde, ohne etwas zu veraendern:\n"
                "• Es wird nichts kopiert, verschoben oder umbenannt.\n"
                "• Es entsteht keine _index.txt, deshalb gibt ein Trockenlauf den Tab "
                '"Bereinigen" nicht frei.\n'
                "• Die geplanten Aktionen stehen im Log und in _log_dry.txt.\n\n"
                "Trotzdem liest der Trockenlauf den Zielordner und legt einen Hash-Cache im "
                "App-Verzeichnis ab. Der naechste echte Lauf nutzt diesen Cache und loescht ihn "
                "anschliessend wieder. Das spart beim zweiten Durchlauf viel Zeit."
            ),
        },
        {
            "id": "dedup",
            "title": "8. Duplikate bereinigen",
            "text": (
                'Der Tab "Bereinigen" raeumt die beim Sortieren entstandenen Namensdubletten '
                "auf. Er arbeitet ausschliesslich im Zielordner und ist erst freigeschaltet, "
                "wenn dort ein echter Sortierlauf stattgefunden hat (erkennbar an _index.txt).\n\n"
                "Gruppen: NAME.jpg, NAME_1.jpg, NAME_2.jpg ... gehoeren zusammen.\n\n"
                "Standardregel:\n"
                "• Ist eine _1, _2-Datei byte-identisch mit der Basisdatei, wird sie nach "
                "Duplicates verschoben. Die Basisdatei bleibt im Zielordner.\n"
                "• Die Basisdatei wird einmal pro Gruppe mit nach Duplicates kopiert, damit du "
                "beide Fassungen direkt vergleichen kannst.\n"
                "• Weicht der Inhalt ab, bleibt die Datei unangetastet.\n\n"
                "Erweiterte Regel (Force):\n"
                "• Auch _1, _2-Dateien mit abweichendem Inhalt werden nach Duplicates "
                "verschoben - ohne Inhaltsvergleich. Vorher fragt das Programm nach.\n"
                "• Gedacht fuer Sicherungen mit gleichem Namen und fuer zwei Kameras mit "
                "zufaellig gleichem Dateinamen.\n\n"
                "Fehlt die Basisdatei, wird die kleinste Nummer in den Basisnamen umbenannt "
                "(IMG_1.jpg -> IMG.jpg). Die Datei bleibt im Zielordner.\n\n"
                "Es wird nichts geloescht: Duplicates spiegelt die Ordnerstruktur und wird beim "
                "naechsten Sortieren uebersprungen. Aufraeumen uebernimmst du selbst. Der "
                "Trockenlauf funktioniert auch hier und schreibt nur ins Trockenlauf-Log."
            ),
        },
        {
            "id": "skip",
            "title": "9. Vorhandene Dateien ueberspringen",
            "text": (
                '"Vorhandene Dateien ueberspringen" verhindert, dass _1, _2-Dateien '
                "entstehen: Ist die Zieldatei schon da, bleibt sie unveraendert und die "
                "Quelldatei wird uebersprungen.\n\n"
                "Gedacht ist das fuer Sicherungen, die mit unterschiedlichen Zeitstempeln "
                "abgelegt wurden: Statt einer zweiten Fassung als _1-Datei bleibt die erste "
                "erhalten. Im Log erscheinen solche Dateien als SKIP (existiert) und zaehlen "
                "als Duplikat.\n\n"
                "Ohne diese Option entstehen bei Namensgleichheit _1, _2-Dateien, die du "
                'spaeter im Tab "Bereinigen" pruefen kannst.'
            ),
        },
        {
            "id": "log",
            "title": "10. Log-Fenster",
            "text": (
                "Das Log zeigt alle Aktionen des Laufs, farblich getrennt:\n"
                "• blau: Informationen\n"
                "• gelb: Warnungen\n"
                "• rot: Fehler\n"
                "• gruen: Bericht/Zusammenfassung\n\n"
                "Bedienung:\n"
                '• "Nur Fehler": blendet alles andere aus.\n'
                '• "Auto-Scroll": springt automatisch ans Ende.\n'
                "• Suchfeld + Enter: springt zum naechsten Treffer (Gross-/Kleinschreibung "
                "egal).\n"
                '• "Leeren" (Strg+L), "Speichern" (Strg+S), "Oeffnen".\n\n'
                "Das Log wird auf 50.000 Zeilen begrenzt, damit lange Laeufe keinen Speicher "
                "fuellen. Im Zielordner liegt zusaetzlich _log.txt; im Trockenlauf stattdessen "
                "_log_dry.txt."
            ),
        },
        {
            "id": "settings",
            "title": "11. Einstellungen, Speicherort und Sprache",
            "text": (
                "Gespeichert wird im Benutzerverzeichnis unter ~/.medien_sortierer:\n"
                "• settings.json: Fenstergroesse, Sprache und die zuletzt gewaehlten Ordner\n"
                "• app.log: technisches Programmprotokoll\n\n"
                "Die Einstellungen werden beim Schliessen geschrieben und beim naechsten Start "
                "wieder geladen. Die Sprache wirkt sofort, ohne Neustart.\n\n"
                "Der Zielordner enthaelt nach einem echten Lauf:\n"
                '• _index.txt: Dateiindex fuer schnellere Folgelaeufe und Merkmal "hier wurde '
                'schon sortiert" (schaltet den Tab "Bereinigen" frei)\n'
                "• _log.txt: Protokoll des Laufs\n"
                "• Duplicates: aussortierte Namensdubletten\n\n"
                "Ist die Quelle gleich dem Ziel, sortiert das Programm automatisch in den "
                "Unterordner Sorted. Der Zielordner selbst wird nie als Quelle durchsucht."
            ),
        },
        {
            "id": "keys",
            "title": "12. Tastenkuerzel und Problemloesung",
            "text": (
                "Tastenkuerzel:\n"
                "• F1 - dieses Handbuch oeffnen\n"
                "• F5 - Lauf starten\n"
                "• Esc - Lauf stoppen\n"
                "• Strg+L - Log leeren\n"
                "• Strg+S - Log speichern\n\n"
                "Die kleinen ?-Buttons neben den Gruppen zeigen kurze Hinweise zum jeweiligen "
                "Bereich.\n\n"
                "Wenn etwas nicht wie erwartet laeuft:\n"
                "• Alles landet in _No_Date: Es wurde kein Datum gefunden. Fuer EXIF-Daten "
                "Pillow installieren, fuer Videos ffprobe bereitstellen.\n"
                '• Der Tab "Bereinigen" ist gesperrt: In diesem Ziel gab es noch keinen echten '
                "Sortierlauf. Erst sortieren - ein Trockenlauf reicht nicht.\n"
                '• Dateien heissen _1, _2: Es gab Namensgleichheit. Im Tab "Bereinigen" '
                "aufraeumen.\n"
                "• Nach dem Sortieren fehlen Dateien: Sie waren inhaltlich schon vorhanden und "
                "wurden als Duplikat uebersprungen - das Log zeigt sie als DUP.\n"
                '• Der Lauf bricht mit "Nicht genug Speicherplatz" ab: Platz im Ziel schaffen '
                "oder eine andere Zielplatte waehlen."
            ),
        },
    ],
}
