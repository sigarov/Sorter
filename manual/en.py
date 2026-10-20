"""English manual - translation of the German master in manual/de.py."""

EN = {
    "title": "User Manual",
    "sections": [
        {
            "id": "intro",
            "title": "1. What the program does",
            "text": (
                "The Media Sorter arranges pictures and videos into a fixed folder structure "
                "and then helps you clean up duplicate names.\n\n"
                "You choose one or two sources (folders or entire drives) and a target folder. "
                "The program reads all pictures and videos, determines the capture date and "
                "copies each file into the matching year, month and day folder.\n\n"
                "Good to know:\n"
                "• The sources are only read, never changed.\n"
                '• Nothing is deleted. Duplicates go to the "Duplicates" folder.\n'
                "• The folder names in the target are always English (Pictures, Videos, "
                "_No_Date). This keeps the structure stable when you change the language.\n"
                "• The interface is available in seven languages. This manual appears in the "
                "selected language as soon as a translation exists - until then in German."
            ),
        },
        {
            "id": "start",
            "title": "2. Getting started",
            "text": (
                "1. Choose the language at the top left - the display changes immediately.\n"
                "2. Choose source 1: folder or drive. Optionally add source 2.\n"
                "3. Choose the target: files are sorted there.\n"
                "4. Optionally enable the dry run to simulate beforehand.\n"
                '5. Click "▶  Start" (or press F5).\n\n'
                "During the run two progress bars show the status: first the indexing of the "
                'target, then the sorting. Use "■  Stop" (or Esc) to cancel; files already '
                "copied are kept.\n\n"
                'The "Clean up" tab is only unlocked after a real sorting run in the selected '
                "target."
            ),
        },
        {
            "id": "sort",
            "title": "3. Sorting and folder structure",
            "text": (
                "The sorting run has two phases:\n"
                "1. The target folder is indexed. Size, modification time and checksum (hash) "
                "of all existing files are recorded.\n"
                "2. Each source file is checked and copied into the target folder.\n\n"
                "This is how the date is determined (in this order):\n"
                "• EXIF capture date of the picture (requires Pillow)\n"
                "• Video metadata (requires ffprobe in PATH)\n"
                "• Date from the file name, e.g. 2020-05-17, 20200517 or 20200517_143025\n\n"
                "The file system date is deliberately not used: files without a real timestamp "
                "should end up in the _No_Date folder instead of being sorted incorrectly by "
                "their copy date.\n\n"
                "Structure in the target (example):\n"
                "• Pictures/2020/05/17/holiday.jpg\n"
                "• Videos/2020/05/17/holiday.mp4\n"
                "• _No_Date/Pictures/unknown.jpg\n\n"
                "If a target file already exists and the content is the same, the source file "
                "is skipped. If the name is the same but the content differs, _1, _2 etc. are "
                "created. Before copying, the program checks the free disk space and compares "
                "the file size after copying."
            ),
        },
        {
            "id": "names",
            "title": "4. File names",
            "text": (
                "Six variants for new file names (example: holiday.jpg from 17 May 2020, "
                "14:30:25):\n\n"
                "• Original: holiday.jpg\n"
                "• Date_Name: 20200517_holiday.jpg\n"
                "• Date_Time_Name: 20200517_143025_holiday.jpg\n"
                "• Year-Month-Day_Name: 2020-05-17_holiday.jpg\n"
                "• Number: 00001.jpg\n"
                "• Date_Number: 20200517_0001.jpg\n\n"
                'Without a date, "Number" only assigns the running number; with all other '
                "variants the original name is kept. The extension is always lowercase. If "
                "names collide, the program appends _1, _2, ..."
            ),
        },
        {
            "id": "structure",
            "title": "5. Structure: separate or together",
            "text": (
                "Separate (default): pictures and videos are in their own trees.\n"
                "  Pictures/2020/05/17/... and Videos/2020/05/17/...\n"
                "Together: both go into the same year/month/day folder.\n"
                "  2020/05/17/...\n\n"
                "Granularity:\n"
                "• Year: 2020/\n"
                "• Month: 2020/05/\n"
                "• Day: 2020/05/17/\n\n"
                'Files without a date go to _No_Date - with "Separate" additionally under '
                "Pictures or Videos. There, _liste.txt lists all affected files."
            ),
        },
        {
            "id": "filters",
            "title": "6. Filtering folders",
            "text": (
                "The filter field limits which subfolders of the source are searched.\n"
                "• Separate multiple terms with commas: Photos, Pictures, DCIM\n"
                "• Only folder names count, not file extensions.\n"
                "• Case does not matter.\n"
                "• A match also applies to all subfolders.\n"
                "• Empty field = entire source.\n\n"
                'Example: D:\\Backup contains "Photos", "Documents" and "Videos". With the '
                'filter "Photos, Videos" only those two folders are read.\n\n'
                'The "Clean up" tab has no filter: the whole target folder is always checked '
                "there."
            ),
        },
        {
            "id": "dryrun",
            "title": "7. Dry run and index cache",
            "text": (
                "The dry run shows what would happen without changing anything:\n"
                "• Nothing is copied, moved or renamed.\n"
                '• No _index.txt is created, so a dry run does not unlock the "Clean up" '
                "tab.\n"
                "• The planned actions appear in the log and in _log_dry.txt.\n\n"
                "Nevertheless, the dry run reads the target folder and stores a hash cache in "
                "the app directory. The next real run uses this cache and deletes it "
                "afterwards. This saves a lot of time on the second pass."
            ),
        },
        {
            "id": "dedup",
            "title": "8. Cleaning up duplicates",
            "text": (
                'The "Clean up" tab removes the duplicate names created during sorting. It '
                "works exclusively in the target folder and is only unlocked once a real "
                "sorting run has taken place there (recognisable by _index.txt).\n\n"
                "Groups: NAME.jpg, NAME_1.jpg, NAME_2.jpg ... belong together.\n\n"
                "Standard rule:\n"
                "• If a _1, _2 file is byte-identical to the base file, it is moved to "
                "Duplicates. The base file stays in the target folder.\n"
                "• The base file is copied to Duplicates once per group so that you can compare "
                "both versions directly.\n"
                "• If the content differs, the file is left untouched.\n\n"
                "Extended rule (Force):\n"
                "• _1, _2 files with differing content are also moved to Duplicates - without "
                "comparing the content. The program asks for confirmation first.\n"
                "• Intended for backups with the same name and for two cameras with "
                "accidentally identical file names.\n\n"
                "If the base file is missing, the lowest number is renamed to the base name "
                "(IMG_1.jpg -> IMG.jpg). The file stays in the target folder.\n\n"
                "Nothing is deleted: Duplicates mirrors the folder structure and is skipped "
                "during the next sorting run. You do the cleanup yourself. The dry run also "
                "works here and only writes to the dry-run log."
            ),
        },
        {
            "id": "skip",
            "title": "9. Skipping existing files",
            "text": (
                '"Skip existing files" prevents _1, _2 files from being created: if the '
                "target file already exists, it remains unchanged and the source file is "
                "skipped.\n\n"
                "This is intended for backups saved with different timestamps: instead of "
                "creating a second version as a _1 file, the first one is kept. In the log, "
                "such files appear as SKIP (exists) and count as a duplicate.\n\n"
                "Without this option, files with the same name become _1, _2 files, which you "
                'can check later in the "Clean up" tab.'
            ),
        },
        {
            "id": "log",
            "title": "10. Log window",
            "text": (
                "The log shows all actions of the run, colour-coded:\n"
                "• blue: information\n"
                "• yellow: warnings\n"
                "• red: errors\n"
                "• green: report/summary\n\n"
                "Controls:\n"
                '• "Errors only": hides everything else.\n'
                '• "Auto-scroll": automatically jumps to the end.\n'
                "• Search field + Enter: jumps to the next match (case-insensitive).\n"
                '• "Clear" (Ctrl+L), "Save" (Ctrl+S), "Open".\n\n'
                "The log is limited to 50,000 lines so that long runs do not fill memory. The "
                "target folder also contains _log.txt; in a dry run _log_dry.txt instead."
            ),
        },
        {
            "id": "settings",
            "title": "11. Settings, storage location and language",
            "text": (
                "Data is stored in the user directory under ~/.medien_sortierer:\n"
                "• settings.json: window size, language and the last selected folders\n"
                "• app.log: technical program log\n\n"
                "Settings are written when the program closes and loaded again on the next "
                "start. The language takes effect immediately, without a restart.\n\n"
                "After a real run the target folder contains:\n"
                '• _index.txt: file index for faster subsequent runs and the marker "already '
                'sorted" (unlocks the "Clean up" tab)\n'
                "• _log.txt: log of the run\n"
                "• Duplicates: sorted-out duplicate names\n\n"
                "If the source equals the target, the program automatically sorts into the "
                "Sorted subfolder. The target folder itself is never searched as a source."
            ),
        },
        {
            "id": "keys",
            "title": "12. Keyboard shortcuts and troubleshooting",
            "text": (
                "Keyboard shortcuts:\n"
                "• F1 - open this manual\n"
                "• F5 - start the run\n"
                "• Esc - stop the run\n"
                "• Ctrl+L - clear the log\n"
                "• Ctrl+S - save the log\n\n"
                "The small ? buttons next to the groups show short hints for that area.\n\n"
                "If something does not work as expected:\n"
                "• Everything ends up in _No_Date: no date was found. Install Pillow for EXIF "
                "data and provide ffprobe for videos.\n"
                '• The "Clean up" tab is locked: there has not been a real sorting run in '
                "this target yet. Sort first - a dry run is not enough.\n"
                "• Files are named _1, _2: there was a name collision. Clean up in the "
                '"Clean up" tab.\n'
                "• Files are missing after sorting: they already existed with the same content "
                "and were skipped as duplicates - the log shows them as DUP.\n"
                '• The run aborts with "Not enough disk space": free up space in the target '
                "or choose another target drive."
            ),
        },
    ],
}
