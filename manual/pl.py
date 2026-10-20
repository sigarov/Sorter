"""Instrukcja polska — tłumaczenie niemieckiego oryginału manual/de.py."""

PL = {
    "title": "Instrukcja obsługi",
    "sections": [
        {
            "id": "intro",
            "title": "1. Co robi program",
            "text": (
                "Sortownik mediów układa zdjęcia i filmy w stałą strukturę folderów, a "
                "następnie pomaga uporządkować duplikaty nazw.\n\n"
                "Wybierasz jedno lub dwa źródła (foldery albo całe dyski) oraz folder "
                "docelowy. Program odczytuje wszystkie zdjęcia i filmy, ustala datę wykonania "
                "i kopiuje każdy plik do odpowiedniego folderu roku, miesiąca i dnia.\n\n"
                "Warto wiedzieć:\n"
                "• Źródła są tylko odczytywane, nigdy niezmieniane.\n"
                '• Nic nie jest usuwane. Duplikaty trafiają do folderu "Duplicates".\n'
                "• Nazwy folderów w miejscu docelowym są zawsze angielskie (Pictures, Videos, "
                "_No_Date). Dzięki temu struktura pozostaje stabilna przy zmianie języka.\n"
                "• Interfejs jest dostępny w siedmiu językach. Ta instrukcja pojawia się w "
                "wybranym języku, gdy tylko istnieje tłumaczenie — do tego czasu po niemiecku."
            ),
        },
        {
            "id": "start",
            "title": "2. Pierwsze kroki",
            "text": (
                "1. Wybierz język w lewym górnym rogu — widok zmienia się od razu.\n"
                "2. Wybierz źródło 1: folder lub dysk. W razie potrzeby dodaj źródło 2.\n"
                "3. Wybierz cel: tam zostaną posortowane pliki.\n"
                "4. W razie potrzeby włącz próbę na sucho, aby najpierw zasymulować.\n"
                '5. Kliknij "▶  Start" (lub naciśnij F5).\n\n'
                "Podczas pracy dwa paski postępu pokazują stan: najpierw indeksowanie celu, "
                'potem sortowanie. Przycisk "■  Stop" (lub Esc) przerywa pracę; już '
                "skopiowane pliki pozostają.\n\n"
                'Karta "Czyść" jest odblokowana dopiero po rzeczywistym sortowaniu w '
                "wybranym celu."
            ),
        },
        {
            "id": "sort",
            "title": "3. Sortowanie i struktura folderów",
            "text": (
                "Sortowanie składa się z dwóch etapów:\n"
                "1. Folder docelowy jest indeksowany. Zapisywane są rozmiar, czas modyfikacji "
                "i suma kontrolna (hash) wszystkich istniejących plików.\n"
                "2. Każdy plik źródłowy jest sprawdzany i kopiowany do folderu docelowego.\n\n"
                "Data jest ustalana w tej kolejności:\n"
                "• Data wykonania EXIF zdjęcia (wymaga Pillow)\n"
                "• Metadane filmu (wymaga ffprobe w PATH)\n"
                "• Data z nazwy pliku, np. 2020-05-17, 20200517 lub 20200517_143025\n\n"
                "Data systemu plików celowo nie jest używana: pliki bez rzeczywistego znacznika "
                "czasu mają trafiać do folderu _No_Date, zamiast być błędnie sortowane według "
                "daty kopiowania.\n\n"
                "Struktura w celu (przykład):\n"
                "• Pictures/2020/05/17/wakacje.jpg\n"
                "• Videos/2020/05/17/wakacje.mp4\n"
                "• _No_Date/Pictures/nieznany.jpg\n\n"
                "Jeśli plik docelowy już istnieje, a zawartość jest taka sama, plik źródłowy "
                "jest pomijany. Przy tej samej nazwie, ale innej zawartości powstają _1, _2 "
                "itd. Przed kopiowaniem program sprawdza wolne miejsce, a po kopiowaniu "
                "porównuje rozmiar pliku."
            ),
        },
        {
            "id": "names",
            "title": "4. Nazwy plików",
            "text": (
                "Sześć wariantów nowych nazw plików (przykład: wakacje.jpg z 17.05.2020, "
                "14:30:25):\n\n"
                "• Oryginał: wakacje.jpg\n"
                "• Data_Nazwa: 20200517_wakacje.jpg\n"
                "• Data_Czas_Nazwa: 20200517_143025_wakacje.jpg\n"
                "• Rok-Miesiąc-Dzień_Nazwa: 2020-05-17_wakacje.jpg\n"
                "• Numer: 00001.jpg\n"
                "• Data_Numer: 20200517_0001.jpg\n\n"
                'Bez daty "Numer" nadaje tylko numer bieżący; w pozostałych wariantach '
                "zachowywana jest oryginalna nazwa. Rozszerzenie jest zawsze pisane małymi "
                "literami. Przy tej samej nazwie program dodaje _1, _2, ..."
            ),
        },
        {
            "id": "structure",
            "title": "5. Struktura: oddzielnie czy razem",
            "text": (
                "Oddzielnie (domyślnie): zdjęcia i filmy są w osobnych drzewach.\n"
                "  Pictures/2020/05/17/... i Videos/2020/05/17/...\n"
                "Razem: oba trafiają do tego samego folderu rok/miesiąc/dzień.\n"
                "  2020/05/17/...\n\n"
                "Szczegółowość:\n"
                "• Rok: 2020/\n"
                "• Miesiąc: 2020/05/\n"
                "• Dzień: 2020/05/17/\n\n"
                'Pliki bez daty trafiają do _No_Date — przy opcji "Oddzielnie" dodatkowo '
                "pod Pictures lub Videos. Tam plik _liste.txt wymienia wszystkie dotyczące "
                "pliki."
            ),
        },
        {
            "id": "filters",
            "title": "6. Filtrowanie folderów",
            "text": (
                "Pole filtra ogranicza, które podfoldery źródła są przeszukiwane.\n"
                "• Kilka pojęć oddzielaj przecinkami: Zdjęcia, Pictures, DCIM\n"
                "• Liczą się tylko nazwy folderów, nie rozszerzenia plików.\n"
                "• Wielkość liter nie ma znaczenia.\n"
                "• Dopasowanie dotyczy także wszystkich podfolderów.\n"
                "• Puste pole = całe źródło.\n\n"
                'Przykład: w D:\\Backup są "Zdjęcia", "Dokumenty" i "Filmy". Z filtrem '
                '"Zdjęcia, Filmy" odczytywane są tylko te dwa foldery.\n\n'
                'Karta "Czyść" nie ma filtra: tam zawsze sprawdzany jest cały folder docelowy.'
            ),
        },
        {
            "id": "dryrun",
            "title": "7. Próba na sucho i pamięć podręczna indeksu",
            "text": (
                "Próba na sucho pokazuje, co by się stało, bez zmieniania czegokolwiek:\n"
                "• Nic nie jest kopiowane, przenoszone ani zmieniane.\n"
                "• Nie powstaje _index.txt, dlatego próba na sucho nie odblokowuje karty "
                '"Czyść".\n'
                "• Planowane działania są widoczne w dzienniku i w _log_dry.txt.\n\n"
                "Mimo to próba na sucho odczytuje folder docelowy i zapisuje pamięć podręczną "
                "hashy w folderze aplikacji. Następne rzeczywiste uruchomienie korzysta z tej "
                "pamięci i potem ją usuwa. Oszczędza to dużo czasu przy drugim przebiegu."
            ),
        },
        {
            "id": "dedup",
            "title": "8. Czyszczenie duplikatów",
            "text": (
                'Karta "Czyść" usuwa duplikaty nazw powstałe podczas sortowania. Działa '
                "wyłącznie w folderze docelowym i jest odblokowana dopiero po rzeczywistym "
                "sortowaniu w tym folderze (rozpoznawalnym po _index.txt).\n\n"
                "Grupy: NAME.jpg, NAME_1.jpg, NAME_2.jpg ... należą do siebie.\n\n"
                "Reguła standardowa:\n"
                "• Jeśli plik _1, _2 jest identyczny bajtowo z plikiem bazowym, jest "
                "przenoszony do Duplicates. Plik bazowy pozostaje w folderze docelowym.\n"
                "• Plik bazowy jest raz na grupę kopiowany do Duplicates, aby można było "
                "bezpośrednio porównać obie wersje.\n"
                "• Jeśli zawartość się różni, plik pozostaje nietknięty.\n\n"
                "Reguła rozszerzona (Force):\n"
                "• Pliki _1, _2 o różnej zawartości również są przenoszone do Duplicates — bez "
                "porównywania zawartości. Wcześniej program prosi o potwierdzenie.\n"
                "• Przewidziana dla kopii zapasowych o tej samej nazwie oraz dla dwóch "
                "aparatów, których nazwy plików przypadkowo się pokrywają.\n\n"
                "Jeśli brakuje pliku bazowego, plik o najniższym numerze jest zmieniany na nazwę "
                "bazową (IMG_1.jpg -> IMG.jpg). Plik pozostaje w folderze docelowym.\n\n"
                "Nic nie jest usuwane: Duplicates odwzorowuje strukturę folderów i jest "
                "pomijany przy następnym sortowaniu. Porządkowanie wykonujesz sam. Próba na "
                "sucho działa także tutaj i zapisuje tylko do dziennika próby."
            ),
        },
        {
            "id": "skip",
            "title": "9. Pomijanie istniejących plików",
            "text": (
                '"Pomiń istniejące pliki" zapobiega tworzeniu plików _1, _2: jeśli plik '
                "docelowy już istnieje, pozostaje bez zmian, a plik źródłowy jest pomijany.\n\n"
                "Opcja jest przeznaczona dla kopii zapasowych zapisanych z różnymi znacznikami "
                "czasu: zamiast tworzyć drugą wersję jako plik _1, zachowywana jest pierwsza. "
                "W dzienniku takie pliki pojawiają się jako SKIP (istnieje) i liczą się jako "
                "duplikaty.\n\n"
                "Bez tej opcji przy tej samej nazwie powstają pliki _1, _2, które można później "
                'sprawdzić na karcie "Czyść".'
            ),
        },
        {
            "id": "log",
            "title": "10. Okno dziennika",
            "text": (
                "Dziennik pokazuje wszystkie działania przebiegu, oznaczone kolorami:\n"
                "• niebieski: informacje\n"
                "• żółty: ostrzeżenia\n"
                "• czerwony: błędy\n"
                "• zielony: raport/podsumowanie\n\n"
                "Obsługa:\n"
                '• "Tylko błędy": ukrywa wszystko inne.\n'
                '• "Auto-przewijanie": automatycznie przechodzi na koniec.\n'
                "• Pole wyszukiwania + Enter: przechodzi do następnego trafienia (bez "
                "rozróżniania wielkości liter).\n"
                '• "Wyczyść" (Ctrl+L), "Zapisz" (Ctrl+S), "Otwórz".\n\n'
                "Dziennik jest ograniczony do 50 000 wierszy, aby długie przebiegi nie "
                "zapełniały pamięci. W folderze docelowym znajduje się dodatkowo _log.txt; w "
                "próbie na sucho zamiast niego _log_dry.txt."
            ),
        },
        {
            "id": "settings",
            "title": "11. Ustawienia, lokalizacja i język",
            "text": (
                "Dane są zapisywane w katalogu użytkownika w ~/.medien_sortierer:\n"
                "• settings.json: rozmiar okna, język i ostatnio wybrane foldery\n"
                "• app.log: techniczny dziennik programu\n\n"
                "Ustawienia są zapisywane przy zamknięciu i wczytywane przy następnym "
                "uruchomieniu. Język działa od razu, bez ponownego startu.\n\n"
                "Po rzeczywistym przebiegu folder docelowy zawiera:\n"
                "• _index.txt: indeks plików dla szybszych kolejnych przebiegów i znacznik "
                '"już posortowano" (odblokowuje kartę "Czyść")\n'
                "• _log.txt: dziennik przebiegu\n"
                "• Duplicates: odłożone duplikaty nazw\n\n"
                "Jeśli źródło jest takie samo jak cel, program automatycznie sortuje do "
                "podfolderu Sorted. Sam folder docelowy nigdy nie jest przeszukiwany jako "
                "źródło."
            ),
        },
        {
            "id": "keys",
            "title": "12. Skróty klawiszowe i rozwiązywanie problemów",
            "text": (
                "Skróty klawiszowe:\n"
                "• F1 — otwórz tę instrukcję\n"
                "• F5 — uruchom przebieg\n"
                "• Esc — zatrzymaj przebieg\n"
                "• Ctrl+L — wyczyść dziennik\n"
                "• Ctrl+S — zapisz dziennik\n\n"
                "Małe przyciski ? obok grup pokazują krótkie wskazówki dotyczące danego "
                "obszaru.\n\n"
                "Jeśli coś nie działa zgodnie z oczekiwaniami:\n"
                "• Wszystko trafia do _No_Date: nie znaleziono daty. Zainstaluj Pillow dla "
                "danych EXIF, a dla filmów udostępnij ffprobe.\n"
                '• Karta "Czyść" jest zablokowana: w tym celu nie było jeszcze rzeczywistego '
                "sortowania. Najpierw posortuj — próba na sucho nie wystarczy.\n"
                "• Pliki nazywają się _1, _2: doszło do kolizji nazw. Uporządkuj je na karcie "
                '"Czyść".\n'
                "• Po sortowaniu brakuje plików: istniały już z tą samą zawartością i zostały "
                "pominięte jako duplikaty — dziennik pokazuje je jako DUP.\n"
                '• Przebieg przerywa się komunikatem "Za mało miejsca na dysku": zwolnij '
                "miejsce w celu lub wybierz inny dysk docelowy."
            ),
        },
    ],
}
