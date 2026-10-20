"""GUI (App) fuer den Sortierer."""

import logging
import os
import queue
import re
import threading
import tkinter as tk
from collections import deque
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

from config import (
    BILD_EXT,
    FOLDER_NO_DATE,
    GRAN_OPTIONS,
    NAMING_OPTIONS,
    SORT_UNTERORDNER,
    STRUCT_OPTIONS,
    VIDEO_EXT,
    WINDOW_TITLE,
    app_dir,
    ist_dupes_ordner,
)
from dedup_sorter import DedupSorter
from help_texts import get_help
from manual import get_manual
from sorter import Sorter
from translations import TRANSLATIONS
from utils import lesbare_groesse

log = logging.getLogger(__name__)

LANG_CODES = ["en", "de", "ru", "fr", "es", "pl", "tr"]

# Obergrenze fuer Log-Zeilen (im Puffer und im Text-Widget), damit sehr
# lange Laeufe den Speicher nicht unbegrenzt fuellen.
MAX_LOG_ZEILEN = 50000


def _enable_dpi_awareness():
    """Aktiviert DPI-Bewusstsein unter Windows (scharfe Schrift auf HiDPI)."""
    if os.name != "nt":
        return
    try:
        from ctypes import windll
    except Exception:
        return
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class App(tk.Tk):
    def __init__(self):
        _enable_dpi_awareness()
        super().__init__()
        self._init_vars()
        self._init_window()
        self._build_ui()

        self._apply_language()
        self._on_dedup_toggle()

        self.after(200, self.poll_log)
        self.after(1000, self._aktualisiere_zeiten)

        self._load_settings()
        self._bind_shortcuts()
        # Dedup erst freigeben, wenn im Ziel schon sortiert wurde.
        self._aktualisiere_dedup_freigabe()
        self._ui_ready = True
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._set_status(self.lang.get("status_ready", "Bereit"))

    def _init_vars(self):
        self._log_lines = deque(maxlen=MAX_LOG_ZEILEN)
        self._log_only_errors = tk.BooleanVar(value=False)
        self._log_autoscroll = tk.BooleanVar(value=True)
        self._log_search = tk.StringVar()
        self.status_text = tk.StringVar(value="")
        self._settings = {}
        self._syncing_mode = False
        self._ui_ready = False
        self.lang_code = "de"
        self.lang = TRANSLATIONS[self.lang_code]

        self.q1 = tk.StringVar()
        self.q2 = tk.StringVar()
        self.ziel = tk.StringVar()
        self.filter1 = tk.StringVar()
        self.filter2 = tk.StringVar()
        self.trockenlauf = tk.BooleanVar(value=False)
        self.skip_existing = tk.BooleanVar(value=False)
        self.dedup = tk.BooleanVar(value=False)
        self.dedup_force = tk.BooleanVar(value=False)
        self.gemeinsam = tk.BooleanVar(value=False)
        self.naming_label = tk.StringVar()
        self.gran_label = tk.StringVar()
        self.struct_label = tk.StringVar()
        self.lang_display = tk.StringVar()
        self._aktueller_naming_key = "original"
        self._aktueller_gran_key = "year"
        self._aktueller_struct_key = "separate"

        self.log_q = queue.Queue()
        self.stop_event = threading.Event()
        self._last_paths = {}
        self.start_zeit = None
        self.phase_start = None
        self._phase_aktiv = None
        self.ende_zeit = None

        self._idx_state = None
        self._sort_state = None

        self._manual_win = None
        self._manual_index = 0
        self._manual_toc = None
        self._manual_txt = None

        self._text_widgets = {}

    def _init_window(self):
        self.geometry("920x800")
        self.resizable(True, True)
        self.minsize(800, 680)
        self.configure(padx=12, pady=10)

    def _build_ui(self):
        self._build_language_bar()

        fr_main = tk.Frame(self)
        fr_main.pack(fill="x", pady=(0, 6))
        fr_main.columnconfigure(0, weight=1, uniform="col")
        fr_main.columnconfigure(1, weight=1, uniform="col")

        left_col = tk.Frame(fr_main)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self._build_sources_column(left_col)
        self._build_options_column(fr_main)

        self._build_separator()
        self._build_log_panel()
        self._build_status_bar()

    def _build_language_bar(self):
        # ---------- Sprache (oben) ----------
        fr_lang = tk.Frame(self)
        fr_lang.pack(fill="x", pady=(0, 6))
        self._text_widgets["lbl_lang"] = tk.Label(fr_lang, text="", font=("", 10, "bold"))
        self._text_widgets["lbl_lang"].pack(side="left")
        self.cmb_lang = ttk.Combobox(
            fr_lang,
            textvariable=self.lang_display,
            values=[TRANSLATIONS[c]["name"] for c in LANG_CODES],
            state="readonly",
            width=15,
        )
        self.cmb_lang.pack(side="left", padx=6)
        self.cmb_lang.bind("<<ComboboxSelected>>", self._on_lang_change)

        self.btn_help = tk.Button(
            fr_lang,
            text="",
            font=("", 9, "bold"),
            relief="raised",
            bd=1,
            cursor="hand2",
            command=self._open_manual,
        )
        self.btn_help.pack(side="right")

    def _build_sources_column(self, parent):
        self.q1_entry, self.btn_w1, self.filter1_entry = self._build_source_block(
            parent, 1, self.q1, self.filter1
        )
        self.q2_entry, self.btn_w2, self.filter2_entry = self._build_source_block(
            parent, 2, self.q2, self.filter2, pady=(10, 0)
        )
        self._build_target_block(parent)
        self._build_action_buttons(parent)
        self._build_progress_bars(parent)

    def _build_source_block(self, parent, nummer, pfad_var, filter_var, pady=(0, 0)):
        """Baut einen Quellblock (Pfad, Waehlen-Button, Filter, Hinweis)."""
        block = tk.Frame(parent)
        block.pack(fill="x", pady=pady)

        label = tk.Label(block, text="", font=("", 10, "bold"))
        label.pack(anchor="w")
        self._text_widgets[f"lbl_source{nummer}"] = label

        row = tk.Frame(block)
        row.pack(fill="x", pady=(0, 3))
        entry = tk.Entry(row, textvariable=pfad_var)
        entry.pack(side="left", fill="x", expand=True)
        button = tk.Button(row, text="", command=lambda v=pfad_var: self.waehle(v))
        button.pack(side="left", padx=(4, 0))

        filter_label = tk.Label(block, text="", fg="#444")
        filter_label.pack(anchor="w")
        self._text_widgets[f"lbl_filter{nummer}"] = filter_label

        filter_entry = tk.Entry(block, textvariable=filter_var)
        filter_entry.pack(fill="x", pady=(0, 1))

        hint = tk.Label(block, text="", fg="#888", font=("", 8))
        hint.pack(anchor="w")
        self._text_widgets[f"lbl_filter_hint{nummer}"] = hint

        return entry, button, filter_entry

    def _build_target_block(self, parent):
        left3 = tk.Frame(parent)
        left3.pack(fill="x", pady=(10, 0))
        self._text_widgets["lbl_target"] = tk.Label(left3, text="", font=("", 10, "bold"))
        self._text_widgets["lbl_target"].pack(anchor="w")
        self.ziel_frame = tk.Frame(left3)
        self.ziel_frame.pack(fill="x", pady=(0, 3))
        self.ziel_entry = tk.Entry(self.ziel_frame, textvariable=self.ziel)
        self.ziel_entry.pack(side="left", fill="x", expand=True)
        self.btn_w3 = tk.Button(self.ziel_frame, text="", command=lambda: self.waehle(self.ziel))
        self.btn_w3.pack(side="left", padx=(4, 0))
        # Ziel auch bei manueller Eingabe neu bewerten (Dedup-Freigabe).
        self.ziel_entry.bind("<KeyRelease>", lambda _e: self._aktualisiere_dedup_freigabe())
        self.ziel_entry.bind("<FocusOut>", lambda _e: self._aktualisiere_dedup_freigabe())

    def _build_action_buttons(self, parent):
        btn_box = tk.Frame(parent)
        btn_box.pack(fill="x", pady=(8, 12))
        self.btn_start = tk.Button(
            btn_box,
            text="",
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            font=("", 11, "bold"),
            relief="raised",
            bd=2,
            command=self.start,
        )
        self.btn_start.pack(side="left", ipadx=20)
        self.btn_stop = tk.Button(
            btn_box,
            text="",
            state="disabled",
            bg="#F44336",
            fg="white",
            activebackground="#D32F2F",
            activeforeground="white",
            disabledforeground="#eeeeee",
            font=("", 11, "bold"),
            relief="raised",
            bd=2,
            command=self.stoppen,
        )
        self.btn_stop.pack(side="left", padx=8)

    def _build_progress_bars(self, parent):
        idx_box = tk.Frame(parent)
        self.lbl_index = tk.Label(idx_box, text="", font=("", 9), fg="#555")
        self.lbl_index.pack(anchor="w")
        self.progress_index = ttk.Progressbar(idx_box, mode="determinate")
        self.progress_index.pack(fill="x", pady=(2, 0))

        srt_box = tk.Frame(parent)
        self.lbl_sort = tk.Label(srt_box, text="", font=("", 9), fg="#555")
        self.lbl_sort.pack(anchor="w")
        self.progress = ttk.Progressbar(srt_box, mode="determinate")
        self.progress.pack(fill="x", pady=(2, 0))

        # von unten her anordnen: Sortierung ganz unten, Ziel-Index darueber
        srt_box.pack(side="bottom", fill="x")
        idx_box.pack(side="bottom", fill="x", pady=(0, 6))

    def _build_options_column(self, fr_main):
        # ================= RECHTE SPALTE: Optionen in Gruppen =================
        right_col = tk.Frame(fr_main)
        right_col.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self._build_general_group(right_col)
        self._build_mode_tabs(right_col)
        self._build_dedup_group(self.tab_dedup)
        self._build_naming_group(self.tab_sort)

    def _build_general_group(self, parent):
        """Gruppe "Allgemein" mit Trockenlauf und Ueberspringen."""
        self.grp_general = tk.LabelFrame(
            parent, text="", bd=3, relief="ridge", padx=8, pady=4, font=("", 9, "bold")
        )
        self.grp_general.pack(fill="x", pady=(0, 8))
        self._help_button(self.grp_general, "general")

        self.chk_dry = ttk.Checkbutton(self.grp_general, variable=self.trockenlauf, text="")
        self.chk_dry.pack(anchor="w")

        self.chk_skip = ttk.Checkbutton(self.grp_general, variable=self.skip_existing, text="")
        self.chk_skip.pack(anchor="w")

    def _build_mode_tabs(self, parent):
        """Notebook mit den Tabs "Sortieren" und "Bereinigen"."""
        self.nb = ttk.Notebook(parent)
        self.nb.pack(fill="both", expand=True)
        self.tab_sort = tk.Frame(self.nb)
        self.tab_dedup = tk.Frame(self.nb)
        self.nb.add(self.tab_sort, text="")
        self.nb.add(self.tab_dedup, text="")
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _build_dedup_group(self, parent):
        """Dedup-Optionen im Tab "Bereinigen" (Modus wird ueber den Tab gewaehlt)."""
        self.grp_dedup = tk.LabelFrame(
            parent, text="", bd=3, relief="ridge", padx=8, pady=4, font=("", 9, "bold")
        )
        self.grp_dedup.pack(fill="both", expand=True, padx=2, pady=2)
        self._help_button(self.grp_dedup, "dedup")

        # Trennlinie zur naechsten Regel (Force)
        ttk.Separator(self.grp_dedup, orient="horizontal").pack(fill="x", pady=(8, 6))

        # Force-Regel (eigene, unabhaengige Zusatzregel)
        self._text_widgets["lbl_dedup_extra"] = tk.Label(
            self.grp_dedup, text="", font=("", 9, "bold")
        )
        self._text_widgets["lbl_dedup_extra"].pack(anchor="w", pady=(0, 2))

        self.chk_dedup_force = ttk.Checkbutton(self.grp_dedup, variable=self.dedup_force, text="")
        self.chk_dedup_force.pack(anchor="w", padx=(0, 0), pady=(0, 4))

        self._text_widgets["lbl_dedup_hint"] = tk.Label(
            self.grp_dedup, text="", fg="#888", font=("", 8), justify="left", wraplength=350
        )
        self._text_widgets["lbl_dedup_hint"].pack(anchor="w", pady=(2, 0))

    def _build_naming_group(self, parent):
        """Optionen fuer Sortierung und Namen im Tab "Sortieren"."""
        self.grp_naming = tk.LabelFrame(
            parent, text="", bd=3, relief="ridge", padx=8, pady=4, font=("", 9, "bold")
        )
        self.grp_naming.pack(fill="both", expand=True, padx=2, pady=2)
        self._help_button(self.grp_naming, "naming")

        self._text_widgets["lbl_naming"] = tk.Label(self.grp_naming, text="", font=("", 9, "bold"))
        self._text_widgets["lbl_naming"].pack(anchor="w", pady=(0, 2))
        self.cmb_naming = ttk.Combobox(
            self.grp_naming, textvariable=self.naming_label, state="readonly"
        )
        self.cmb_naming.pack(fill="x")
        self.cmb_naming.bind("<<ComboboxSelected>>", self._on_naming_change)
        self._text_widgets["lbl_hint"] = tk.Label(
            self.grp_naming, text="", fg="#888", font=("", 8), justify="left", wraplength=350
        )
        self._text_widgets["lbl_hint"].pack(anchor="w", pady=(2, 6))

        fr_struct = tk.Frame(self.grp_naming)
        fr_struct.pack(fill="x", anchor="w")
        self._text_widgets["lbl_structure"] = tk.Label(fr_struct, text="", font=("", 9, "bold"))
        self._text_widgets["lbl_structure"].pack(side="left")
        self.cmb_struct = ttk.Combobox(
            fr_struct, textvariable=self.struct_label, state="readonly", width=24
        )
        self.cmb_struct.pack(side="left", padx=6)
        self.cmb_struct.bind("<<ComboboxSelected>>", self._on_struct_change)

        fr_gran = tk.Frame(self.grp_naming)
        fr_gran.pack(fill="x", anchor="w", pady=(6, 0))
        self._text_widgets["lbl_granularity"] = tk.Label(fr_gran, text="", font=("", 9, "bold"))
        self._text_widgets["lbl_granularity"].pack(side="left")
        self.cmb_gran = ttk.Combobox(
            fr_gran, textvariable=self.gran_label, state="readonly", width=22
        )
        self.cmb_gran.pack(side="left", padx=6)
        self.cmb_gran.bind("<<ComboboxSelected>>", self._on_gran_change)

    def _build_separator(self):
        # ---------- Gestrichelte Trennlinie ----------
        canvas = tk.Canvas(self, height=2, bd=0, highlightthickness=0)
        canvas.pack(fill="x", pady=10)
        canvas.create_line(0, 0, 2000, 0, dash=(4, 4), fill="#888")

    def _build_log_panel(self):
        # ---------- Log ----------
        log_head = tk.Frame(self)
        log_head.pack(fill="x")
        self._text_widgets["lbl_log"] = tk.Label(log_head, text="", font=("", 10, "bold"))
        self._text_widgets["lbl_log"].pack(side="left")
        tk.Button(
            log_head,
            text="?",
            width=2,
            font=("", 8, "bold"),
            relief="flat",
            bd=0,
            fg="#2196F3",
            cursor="hand2",
            command=lambda: self._zeige_hilfe("log"),
        ).pack(side="left", padx=(4, 0))

        bar = tk.Frame(log_head)
        bar.pack(side="right")
        self.btn_log_clear = tk.Button(bar, text="", command=self._log_clear)
        self.btn_log_clear.pack(side="left")
        self.btn_log_save = tk.Button(bar, text="", command=self._log_save)
        self.btn_log_save.pack(side="left", padx=4)
        self.btn_log_open = tk.Button(bar, text="", command=self._log_open)
        self.btn_log_open.pack(side="left")
        self.chk_log_errors = ttk.Checkbutton(
            bar, text="", variable=self._log_only_errors, command=self._toggle_log_filter
        )
        self.chk_log_errors.pack(side="left", padx=(8, 0))
        self.chk_log_autoscroll = ttk.Checkbutton(bar, text="", variable=self._log_autoscroll)
        self.chk_log_autoscroll.pack(side="left", padx=(8, 0))

        search_box = tk.Frame(self)
        search_box.pack(fill="x", pady=(2, 2))
        self._text_widgets["lbl_log_search"] = tk.Label(search_box, text="")
        self._text_widgets["lbl_log_search"].pack(side="left")
        ent = tk.Entry(search_box, textvariable=self._log_search)
        ent.pack(side="left", fill="x", expand=True, padx=(4, 0))
        ent.bind("<Return>", self._log_search_next)

        self.txt = tk.Text(self, height=15, bg="#111", fg="#eee", font=("Consolas", 9))
        self.txt.pack(fill="both", expand=True)

    def _build_status_bar(self):
        # ---------- Statusleiste ----------
        status = tk.Label(
            self,
            textvariable=self.status_text,
            anchor="w",
            fg="#333",
            bd=1,
            relief="sunken",
            padx=6,
        )
        status.pack(fill="x", pady=(4, 0))

        self.txt.tag_config("info", foreground="#8ecae6")
        self.txt.tag_config("warn", foreground="#ffb703")
        self.txt.tag_config("error", foreground="#ef476f")
        self.txt.tag_config("report", foreground="#06d6a0")
        self.txt.tag_config("progress", foreground="#cccccc")

    # ---------- Sprachwechsel ----------
    def _on_lang_change(self, event=None):
        name = self.lang_display.get()
        for code in LANG_CODES:
            if TRANSLATIONS[code]["name"] == name:
                self.lang_code = code
                break
        self.lang = TRANSLATIONS[self.lang_code]
        self._apply_language()

    def _apply_language(self):
        self.title(self.lang.get("window_title", WINDOW_TITLE))
        if self._manual_win is not None:
            # Offenes Handbuch in der neuen Sprache neu aufbauen.
            self._open_manual()
        self._apply_language_groups()
        self._apply_language_header()
        self._apply_language_sources()
        self._apply_language_options()
        self._apply_language_tabs()
        self._apply_language_log()
        self._refresh_progress_labels()

    def _apply_language_groups(self):
        L = self.lang
        self.grp_general.config(text=L.get("lbl_group_general", "General"))
        self.grp_dedup.config(text=L.get("lbl_group_dedup", "Deduplication"))
        self.grp_naming.config(text=L.get("lbl_group_naming", "Sorting & Names"))

    def _apply_language_header(self):
        L = self.lang
        self._text_widgets["lbl_lang"].config(text=L["lang_label"])
        self.lang_display.set(L["name"])
        self.btn_help.config(text=L.get("btn_help", "Hilfe"))

    def _update_source_labels(self):
        """Quell- und Zielbeschriftungen passend zum aktiven Modus setzen."""
        L = self.lang
        self._text_widgets["lbl_source1"].config(text=L["lbl_source1"])
        self._text_widgets["lbl_source2"].config(text=L["lbl_source2"])
        self._text_widgets["lbl_target"].config(
            text=L.get("lbl_target_dedup", L["lbl_target"]) if self.dedup.get() else L["lbl_target"]
        )

    def _apply_language_sources(self):
        L = self.lang
        self._update_source_labels()
        self._text_widgets["lbl_filter1"].config(text=L["lbl_filter_short"])
        self._text_widgets["lbl_filter2"].config(text=L["lbl_filter_short"])
        self._text_widgets["lbl_filter_hint1"].config(text=L["lbl_filter_hint"])
        self._text_widgets["lbl_filter_hint2"].config(text=L["lbl_filter_hint"])

        self.btn_w1.config(text=L["btn_choose"])
        self.btn_w2.config(text=L["btn_choose"])
        self.btn_w3.config(text=L["btn_choose"])

    def _apply_language_options(self):
        L = self.lang
        self.chk_dry.config(text=L["chk_dryrun"])
        self.chk_skip.config(text=L["chk_skip_existing"])
        self.chk_dedup_force.config(text=L.get("chk_dedup_force", ""))
        self._text_widgets["lbl_dedup_extra"].config(
            text=L.get("lbl_dedup_extra", "Additional rule:")
        )
        self._update_dedup_hint()

        self._text_widgets["lbl_structure"].config(text=L["lbl_structure"])
        self.cmb_struct["values"] = [L[tr_key] for _, tr_key in STRUCT_OPTIONS]
        for key, tr_key in STRUCT_OPTIONS:
            if key == self._aktueller_struct_key:
                self.struct_label.set(L[tr_key])
                break
        self.gemeinsam.set(self._aktueller_struct_key == "together")

        self._text_widgets["lbl_granularity"].config(text=L["lbl_granularity"])
        self.cmb_gran["values"] = [L[tr_key] for _, tr_key in GRAN_OPTIONS]
        for key, tr_key in GRAN_OPTIONS:
            if key == self._aktueller_gran_key:
                self.gran_label.set(L[tr_key])
                break

        self._text_widgets["lbl_naming"].config(text=L["lbl_naming"])
        self._text_widgets["lbl_hint"].config(text=L["hint_text"].format(nodate=FOLDER_NO_DATE))

        self.btn_start.config(text=L["btn_start"])
        self.btn_stop.config(text=L["btn_stop"])

        self.cmb_naming["values"] = [L[tr_key] for _, tr_key in NAMING_OPTIONS]
        for key, tr_key in NAMING_OPTIONS:
            if key == self._aktueller_naming_key:
                self.naming_label.set(L[tr_key])
                break

    def _apply_language_tabs(self):
        L = self.lang
        self.nb.tab(0, text=L.get("mode_sort", "Sortieren"))
        self._setze_tab_titel(self._dedup_freigabe())

    def _apply_language_log(self):
        L = self.lang
        self._text_widgets["lbl_log"].config(text=L["lbl_log"])
        self.btn_log_clear.config(text=L.get("btn_log_clear", "Leeren"))
        self.btn_log_save.config(text=L.get("btn_log_save", "Speichern"))
        self.btn_log_open.config(text=L.get("btn_log_open", "Oeffnen"))
        self.chk_log_errors.config(text=L.get("chk_log_errors", "Nur Fehler"))
        self.chk_log_autoscroll.config(text=L.get("chk_log_autoscroll", "Auto-Scroll"))
        self._text_widgets["lbl_log_search"].config(text=L.get("lbl_log_search", "Suchen:"))

    def _on_naming_change(self, event=None):
        label = self.naming_label.get()
        L = self.lang
        for key, tr_key in NAMING_OPTIONS:
            if L[tr_key] == label:
                self._aktueller_naming_key = key
                break

    def _on_gran_change(self, event=None):
        label = self.gran_label.get()
        L = self.lang
        for key, tr_key in GRAN_OPTIONS:
            if L[tr_key] == label:
                self._aktueller_gran_key = key
                break

    def _on_struct_change(self, event=None):
        label = self.struct_label.get()
        L = self.lang
        for key, tr_key in STRUCT_OPTIONS:
            if L[tr_key] == label:
                self._aktueller_struct_key = key
                self.gemeinsam.set(key == "together")
                break

    def _update_dedup_hint(self):
        if "lbl_dedup_hint" not in self._text_widgets:
            return
        self._text_widgets["lbl_dedup_hint"].config(text=self.lang.get("hint_dedup_move", ""))

    @staticmethod
    def _set_widget_state(widgets, state):
        """Setzt den Zustand mehrerer Widgets und ignoriert bereits zerstoerte."""
        for widget in widgets:
            try:
                widget.config(state=state)
            except tk.TclError:
                pass

    def _on_dedup_toggle(self):
        self._sync_tab()
        dedup = self.dedup.get()

        # Dedup laeuft im **Zielordner**: dort liegen die _1, _2-Dateien aus dem
        # Sortierlauf. Deshalb sind im Dedup-Modus nur die Ziel-Felder aktiv und
        # Quellen samt Filtern gesperrt.
        self._set_widget_state(
            (
                self.q1_entry,
                self.q2_entry,
                self.filter1_entry,
                self.filter2_entry,
                self.btn_w1,
                self.btn_w2,
            ),
            "disabled" if dedup else "normal",
        )
        self._set_widget_state((self.ziel_entry, self.btn_w3), "normal")

        # Force-Checkbox nur bei aktivem Dedup klickbar
        self._set_widget_state((self.chk_dedup_force,), "normal" if dedup else "disabled")
        self._update_dedup_hint()
        self._update_source_labels()

    # ---------- Hilfe (?-Buttons) ----------
    def _help_button(self, parent, section):
        """Kleiner ?-Button, der den Hilfetext zum Abschnitt anzeigt."""
        btn = tk.Button(
            parent,
            text="?",
            width=2,
            font=("", 8, "bold"),
            relief="flat",
            bd=0,
            fg="#2196F3",
            cursor="hand2",
            command=lambda s=section: self._zeige_hilfe(s),
        )
        btn.pack(anchor="e")
        return btn

    def _zeige_hilfe(self, section):
        text = get_help(self.lang_code, section)
        if not text:
            text = self.lang.get("hint_dedup_first_run", "")
        titel_key = {
            "general": "lbl_group_general",
            "dedup": "lbl_group_dedup",
            "naming": "lbl_group_naming",
            "log": "lbl_log",
        }.get(section, "dlg_help_title")
        titel = self.lang.get(titel_key) or self.lang.get("dlg_help_title", "Hilfe")
        messagebox.showinfo(titel.rstrip(": "), text)

    # ---------- Handbuch (Hilfe-Button / F1) ----------
    def _manual_geometry(self):
        """Fenstergroesse und Position des Handbuchs, passend zum Bildschirm."""
        breite = min(880, max(560, self.winfo_screenwidth() - 120))
        hoehe = min(720, max(380, self.winfo_screenheight() - 160))
        x = max(0, self.winfo_rootx() + 40)
        y = max(0, self.winfo_rooty() + 40)
        return f"{breite}x{hoehe}+{x}+{y}"

    def _open_manual(self, section_id=None):
        """Oeffnet das Handbuch der aktuellen Sprache (Kapitel optional)."""
        self._close_manual()

        manual = get_manual(self.lang_code)
        sections = manual["sections"]
        L = self.lang

        index = self._manual_index
        if section_id is not None:
            for i, section in enumerate(sections):
                if section["id"] == section_id:
                    index = i
                    break
        if not 0 <= index < len(sections):
            index = 0
        self._manual_index = index

        win = tk.Toplevel(self)
        win.title(f"{manual['title']} - {L.get('window_title', WINDOW_TITLE)}")
        win.geometry(self._manual_geometry())
        win.minsize(560, 380)
        self._manual_win = win
        win.protocol("WM_DELETE_WINDOW", self._close_manual)
        win.bind("<Escape>", lambda _e: self._close_manual())

        body = tk.Frame(win, padx=8, pady=8)
        body.pack(fill="both", expand=True)

        toc_frame = tk.Frame(body)
        toc_frame.pack(side="left", fill="y")
        toc = tk.Listbox(toc_frame, width=30, exportselection=False, activestyle="none")
        toc_scroll = ttk.Scrollbar(toc_frame, orient="vertical", command=toc.yview)
        toc.config(yscrollcommand=toc_scroll.set)
        toc.pack(side="left", fill="y")
        toc_scroll.pack(side="left", fill="y")

        text_frame = tk.Frame(body)
        text_frame.pack(side="left", fill="both", expand=True, padx=(8, 0))
        txt = tk.Text(
            text_frame,
            wrap="word",
            padx=8,
            pady=6,
            font=("", 10),
            state="disabled",
            relief="flat",
        )
        text_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=txt.yview)
        txt.config(yscrollcommand=text_scroll.set)
        txt.pack(side="left", fill="both", expand=True)
        text_scroll.pack(side="left", fill="y")
        txt.tag_configure("heading", font=("", 13, "bold"), spacing3=8)
        self._manual_toc = toc
        self._manual_txt = txt

        footer = tk.Frame(win)
        footer.pack(fill="x", padx=8, pady=(0, 8))
        tk.Button(footer, text=L.get("btn_close", "Schliessen"), command=self._close_manual).pack(
            side="right"
        )

        for section in sections:
            toc.insert("end", section["title"])

        state = {"index": None}

        def zeige(i):
            if not 0 <= i < len(sections) or i == state["index"]:
                return
            state["index"] = i
            self._manual_index = i
            toc.selection_clear(0, "end")
            toc.selection_set(i)
            toc.see(i)
            section = sections[i]
            txt.config(state="normal")
            txt.delete("1.0", "end")
            txt.insert("1.0", section["title"] + "\n\n", "heading")
            txt.insert("end", section["text"])
            txt.config(state="disabled")
            txt.see("1.0")

        def on_select(_event=None):
            auswahl = toc.curselection()
            if auswahl:
                zeige(int(auswahl[0]))

        toc.bind("<<ListboxSelect>>", on_select)
        zeige(index)
        win.focus_set()

    def _close_manual(self):
        """Schliesst das Handbuch-Fenster, falls es offen ist."""
        win = self._manual_win
        self._manual_win = None
        self._manual_toc = None
        self._manual_txt = None
        if win is not None:
            try:
                win.destroy()
            except tk.TclError:
                pass

    # ---------- Modus / Tabs ----------
    def _on_tab_change(self, event=None):
        if not getattr(self, "_ui_ready", False):
            return
        if getattr(self, "_syncing_mode", False):
            return
        try:
            idx = self.nb.index(self.nb.select())
        except Exception:
            return
        new_dedup = idx == 1
        if new_dedup and not self._dedup_freigabe():
            # Noch nicht sortiert: zurueck zum Sortieren und erklaeren, warum.
            self._syncing_mode = True
            try:
                self.nb.select(0)
            finally:
                self._syncing_mode = False
            self._setze_tab_titel(False)
            L = self.lang
            messagebox.showinfo(
                L.get("lbl_group_dedup", "Duplikate"),
                L.get("hint_dedup_locked", ""),
            )
            return
        self._setze_tab_titel(True)
        if self.dedup.get() != new_dedup:
            self.dedup.set(new_dedup)
            self._on_dedup_toggle()

    def _sync_tab(self):
        if getattr(self, "_syncing_mode", False):
            return
        nb = self.__dict__.get("nb")
        if nb is None:
            return
        want = 1 if self.dedup.get() else 0
        try:
            if nb.index(nb.select()) != want:
                self._syncing_mode = True
                nb.select(want)
                self._syncing_mode = False
        except Exception:
            self._syncing_mode = False

    # ---------- Log ----------
    def _append_log(self, text, tag):
        self._log_lines.append((tag, text))
        if self._log_only_errors.get() and tag not in ("error", "warn", "report"):
            return
        self.txt.insert("end", text + "\n", tag)
        self._trim_log_text()
        if self._log_autoscroll.get():
            self.txt.see("end")

    def _trim_log_text(self):
        """Kuerzt das Text-Widget, damit lange Laeufe keinen Speicher fressen."""
        try:
            if int(self.txt.index("end-1c").split(".")[0]) > MAX_LOG_ZEILEN:
                self.txt.delete("1.0", f"{MAX_LOG_ZEILEN // 4}.0")
        except Exception:
            log.debug("Log-Text konnte nicht gekuerzt werden", exc_info=True)

    def _render_log(self):
        self.txt.delete("1.0", "end")
        only = self._log_only_errors.get()
        for tag, text in self._log_lines:
            if only and tag not in ("error", "warn", "report"):
                continue
            self.txt.insert("end", text + "\n", tag)
        if self._log_autoscroll.get():
            self.txt.see("end")

    def _toggle_log_filter(self):
        self._render_log()

    def _log_clear(self):
        self._log_lines.clear()
        try:
            self.txt.delete("1.0", "end")
        except Exception:
            log.debug("Log-Text konnte nicht geleert werden", exc_info=True)

    def _log_save(self):
        p = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text", "*.txt"), ("Alle", "*.*")]
        )
        if not p:
            return
        try:
            with open(p, "w", encoding="utf-8") as f:
                for _tag, text in self._log_lines:
                    f.write(text + "\n")
            self._set_status(p)
        except Exception as e:
            messagebox.showerror(self.lang.get("msg_missing_title", "Fehler"), str(e))

    def _log_open(self):
        p = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("Alle", "*.*")])
        if not p:
            return
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    self._append_log(line.rstrip("\n"), "info")
        except Exception as e:
            messagebox.showerror(self.lang.get("msg_missing_title", "Fehler"), str(e))

    def _log_search_next(self, event=None):
        needle = self._log_search.get()
        if not needle:
            return
        self.txt.tag_remove("sel", "1.0", "end")
        idx = self.txt.search(needle, "insert", nocase=True, stopindex="end")
        if not idx:
            idx = self.txt.search(needle, "1.0", nocase=True, stopindex="end")
        if idx:
            end = "%s+%dc" % (idx, len(needle))
            self.txt.tag_add("sel", idx, end)
            self.txt.mark_set("insert", end)
            self.txt.see(idx)

    # ---------- Status / Vorschau / Abschluss ----------
    def _set_status(self, text):
        try:
            self.status_text.set(text)
        except Exception:
            pass

    def _confirm_preview(self, f1, f2):
        quellen = [q for q in (self.q1.get(), self.q2.get()) if q]
        exts = BILD_EXT | VIDEO_EXT
        # Das *effektive* Ziel ueberspringen (bei Quelle = Ziel ist das der
        # Unterordner 'Sorted'). Nur das rohe Ziel zu ueberspringen waere
        # falsch: dann wuerde bei Quelle = Ziel gar nichts gezaehlt.
        ziel_norm = None
        try:
            ziel_norm = os.path.normcase(os.path.abspath(self._effektives_ziel()[0]))
        except Exception:
            ziel_norm = None
        n = 0
        size = 0
        limit = 20000
        for q in quellen:
            for root, dirs, files in os.walk(q):
                # Duplikat-Ordner und den (effektiven) Zielordner nicht mitzaehlen
                dirs[:] = [d for d in dirs if not ist_dupes_ordner(d)]
                if ziel_norm and os.path.normcase(os.path.abspath(root)) == ziel_norm:
                    dirs[:] = []
                    continue
                for fn in files:
                    if os.path.splitext(fn)[1].lower() not in exts:
                        continue
                    n += 1
                    try:
                        size += os.path.getsize(os.path.join(root, fn))
                    except Exception:
                        log.debug(
                            "Groesse fuer %s nicht ermittelbar",
                            os.path.join(root, fn),
                            exc_info=True,
                        )
                    if n >= limit:
                        break
                if n >= limit:
                    break
        if n == 0:
            return True
        size_s = lesbare_groesse(size)
        n_s = ">%d" % limit if n >= limit else str(n)
        L = self.lang
        tmpl = L.get("preview_msg", "{n} Dateien gefunden ({size}).\n\nJetzt starten?")
        # Alle gewaehlten Quellen und das tatsaechliche Ziel anzeigen
        # (bei Quelle = Ziel ist das der Unterordner 'Sorted').
        quelle_text = "; ".join(quellen) or "-"
        ziel_text = self._effektives_ziel()[0] or "-"
        msg = tmpl.format(n=n_s, size=size_s, src=quelle_text, dst=ziel_text)
        return messagebox.askokcancel(L.get("preview_title", "Vorschau"), msg)

    def _show_finish_dialog(self):
        try:
            sorter = getattr(self, "sorter", None)
            stat = getattr(sorter, "stat", None) or {}
            L = self.lang
            # Uebersetzte Report-Zeilen aus dem Log bevorzugen; gibt es keine
            # (z. B. Abbruch), werden Fehler/Warnungen gezeigt. Die rohen
            # stat-Schluessel sind nur der letzte Notnagel.
            zeilen = [t for tag, t in self._log_lines if tag == "report" and t.strip()]
            if not zeilen:
                zeilen = [t for tag, t in self._log_lines if tag in ("error", "warn") and t.strip()]
            if not zeilen:
                zeilen = ["%s: %s" % (k, v) for k, v in stat.items()]
            txt = "\n".join(zeilen)
            dlg = tk.Toplevel(self)
            dlg.title(L.get("dlg_finish_title", "Fertig"))
            dlg.transient(self)
            h = max(4, min(20, len(zeilen) + 1))
            t = tk.Text(dlg, height=h, width=44, bg="#111", fg="#eee", font=("Consolas", 9))
            t.pack(fill="both", expand=True, padx=10, pady=(10, 6))
            t.insert("1.0", txt)
            t.config(state="disabled")
            box = tk.Frame(dlg)
            box.pack(fill="x", padx=10, pady=(0, 10))

            def open_log():
                z = getattr(sorter, "ziel", None)
                cand = [getattr(sorter, "_dry_log_path", None)]
                if z is not None:
                    cand.append(os.path.join(str(z), "_log.txt"))
                for c in cand:
                    if c and os.path.exists(c):
                        self._open_path(c)
                        return
                self._open_path(str(z) if z else os.getcwd())

            def open_folder():
                z = getattr(sorter, "ziel", None)
                self._open_path(str(z) if z else os.getcwd())

            tk.Button(box, text=L.get("btn_open_log", "Log oeffnen"), command=open_log).pack(
                side="left"
            )
            tk.Button(
                box, text=L.get("btn_open_folder", "Ordner oeffnen"), command=open_folder
            ).pack(side="left", padx=6)
            tk.Button(box, text=L.get("btn_close", "Schliessen"), command=dlg.destroy).pack(
                side="right"
            )
        except Exception:
            log.debug("Abschlussdialog fehlgeschlagen", exc_info=True)

    def _open_path(self, path):
        """Oeffnet eine Datei oder einen Ordner mit dem Standardprogramm."""
        import subprocess
        import sys

        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception:
            log.debug("Oeffnen mit Standardprogramm fehlgeschlagen: %s", path, exc_info=True)
            try:
                subprocess.Popen(["explorer", path])
            except Exception:
                log.debug("Auch explorer-Aufruf fehlgeschlagen: %s", path, exc_info=True)

    def _remember_paths(self):
        """Merkt sich den zuletzt gewaehlten Pfad je Feld dauerhaft.

        Die Eingabefelder bleiben beim Start leer; gemerkt wird nur,
        was tatsaechlich gewaehlt oder eingetragen wurde."""
        try:
            for key, var in self._pfad_felder():
                val = var.get().strip()
                if val:
                    self._last_paths[key] = val
            self._save_settings()
        except Exception:
            pass

    def _pfad_felder(self):
        """(Speicher-Schluessel, tk-Variable) der drei Pfadfelder.

        Einzige Quelle der Wahrheit fuer Buttons, Merken und Laden – so koennen
        die Schluessel nicht mehr auseinanderlaufen."""
        return (("q1", self.q1), ("q2", self.q2), ("ziel", self.ziel))

    def _feld_key(self, var):
        """Speicher-Schluessel zu einer Pfad-Variable (oder None)."""
        for key, feld in self._pfad_felder():
            if feld is var:
                return key
        return None

    # ---------- Einstellungen / Shortcuts ----------
    def _settings_path(self):
        return os.path.join(app_dir(), "settings.json")

    @staticmethod
    def _geometry_zerlegen(geo):
        """Zerlegt 'WxH+X+Y' (auch mit negativen Offsets) in Tupel oder None."""
        m = re.match(r"^(\d+)x(\d+)([+-]\d+)([+-]\d+)$", geo or "")
        if not m:
            return None
        return tuple(int(m.group(i)) for i in range(1, 5))

    def _geometrie_passt(self, geo):
        """Grobe Pruefung, ob das gemerkte Fenster sichtbar waere.

        Negative Offsets haengen am rechten/unteren Rand und sind damit immer
        sichtbar; nur bei positiven Offsets wird gegen die Bildschirmgroesse
        geprueft. So landet das Fenster nach einem Monitorwechsel nicht
        ausserhalb des sichtbaren Bereichs."""
        zerlegt = self._geometry_zerlegen(geo)
        if not zerlegt:
            return False
        breite, hoehe, x, y = zerlegt
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        if breite > sw or hoehe > sh:
            return False
        if x >= 0 and x + breite > sw:
            return False
        if y >= 0 and y + hoehe > sh:
            return False
        return True

    def _load_settings(self):
        import json

        try:
            with open(self._settings_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            log.debug("Einstellungen nicht lesbar", exc_info=True)
            data = {}
        self._settings = data if isinstance(data, dict) else {}
        geo = self._settings.get("geometry")
        if geo and self._geometrie_passt(geo):
            try:
                self.geometry(geo)
            except Exception:
                log.debug("Fenstergeometrie nicht anwendbar: %s", geo, exc_info=True)
                pass
        lc = self._settings.get("lang")
        if lc in TRANSLATIONS:
            self.lang_code = lc
            self.lang = TRANSLATIONS[lc]
            self._apply_language()
        lp = self._settings.get("last_paths")
        if isinstance(lp, dict):
            for key, _var in self._pfad_felder():
                val = lp.get(key)
                if val:
                    self._last_paths[key] = val
        # Eingabefelder bleiben beim Start bewusst leer.

    def _save_settings(self):
        import json

        try:
            self._settings["geometry"] = self.winfo_geometry()
            self._settings["lang"] = self.lang_code
            self._settings["last_paths"] = dict(self._last_paths)
            with open(self._settings_path(), "w", encoding="utf-8") as f:
                json.dump(self._settings, f, ensure_ascii=False, indent=2)
        except Exception:
            log.debug("Einstellungen nicht speicherbar", exc_info=True)

    def _on_close(self):
        try:
            self.stop_event.set()
        except Exception:
            pass
        self._remember_paths()
        self._save_settings()
        self.destroy()

    def _bind_shortcuts(self):
        self.bind("<F1>", lambda _e: self._open_manual())
        self.bind("<F5>", lambda e: self.start())
        self.bind("<Escape>", lambda e: self.stoppen())
        self.bind("<Control-l>", lambda e: self._log_clear())
        self.bind("<Control-s>", lambda e: self._log_save())

    # ---------- Sonstiges ----------
    def waehle(self, var, key=None):
        """Oeffnet den Ordner-Dialog im zuletzt fuer dieses Feld genutzten Pfad.

        Ohne ``key`` wird der Schluessel aus der Variable selbst bestimmt
        (siehe ``_pfad_felder()``)."""
        if key is None:
            key = self._feld_key(var)
        initial = (self._last_paths.get(key) if key else None) or var.get().strip() or None
        try:
            if initial and os.path.isdir(initial):
                p = filedialog.askdirectory(initialdir=initial)
            else:
                p = filedialog.askdirectory()
        except Exception:
            p = filedialog.askdirectory()
        if p:
            var.set(p)
            if key:
                self._last_paths[key] = p
            self._remember_paths()
            if key == "ziel":
                # Zielwechsel: Dedup-Freigabe neu bestimmen.
                self._aktualisiere_dedup_freigabe()

    def _dedup_kandidaten(self):
        """Zielordner-Kandidaten fuer Dedup (mit 'Sorted'-Unterordner).

        Wurde mit Quelle = Ziel sortiert, liegt das Ergebnis in '<Ziel>/Sorted'."""
        ziel = self.ziel.get().strip()
        if not ziel:
            return []
        return [ziel, os.path.join(ziel, SORT_UNTERORDNER)]

    def _ziel_mit_index(self):
        """Kandidat, in dem ein Sortierlauf seinen Index hinterlassen hat.

        `_index.txt` schreibt der Sorter am Ende jedes echten Laufs – der
        zuverlaessigste Marker fuer „dort wurde schon sortiert"."""
        for kandidat in self._dedup_kandidaten():
            try:
                if os.path.exists(os.path.join(kandidat, "_index.txt")):
                    return kandidat
            except OSError:
                continue
        return None

    def _dedup_ziel(self):
        """Zielordner fuer den Dedup-Lauf (bevorzugt den sortierten Ordner)."""
        return self._ziel_mit_index() or (self.ziel.get().strip() or None)

    def _dedup_freigabe(self):
        """True, wenn im gewaehlten Ziel schon sortiert wurde."""
        return self._ziel_mit_index() is not None

    def _aktualisiere_dedup_freigabe(self):
        """Sperrt den Dedup-Modus, solange im Ziel noch nicht sortiert wurde."""
        frei = self._dedup_freigabe()

        if not frei and self.__dict__.get("dedup") is not None and self.dedup.get():
            # Modus zuruecknehmen, sonst bliebe der gesperrte Tab aktiv.
            self._syncing_mode = True
            self.dedup.set(False)
            self._syncing_mode = False
            self._on_dedup_toggle()

        self._setze_tab_titel(frei)
        return frei

    def _setze_tab_titel(self, frei):
        """Tab-Beschriftung an die Freigabe anpassen (gesperrt/offen)."""
        nb = self.__dict__.get("nb")
        if nb is None:
            return
        L = self.lang
        try:
            nb.tab(1, text=L["mode_dedup"] if frei else L["mode_dedup_locked"])
        except Exception:
            log.debug("Tab-Titel konnte nicht gesetzt werden", exc_info=True)

    def _effektives_ziel(self):
        """Liefert (ziel, umgeleitet).

        Sind Quelle und Ziel derselbe Ordner, wird in den Unterordner
        'Sorted' umgeleitet, damit die unsortierten Quelldateien nicht
        selbst in den Ziel-Index geraten."""
        ziel = self.ziel.get()
        try:
            zn = os.path.normcase(os.path.abspath(ziel))
        except Exception:
            return ziel, False
        for q in (self.q1.get(), self.q2.get()):
            if not q:
                continue
            try:
                qn = os.path.normcase(os.path.abspath(q))
            except Exception:
                continue
            if qn == zn:
                return os.path.join(ziel, SORT_UNTERORDNER), True
        return ziel, False

    def _bestaetige_start(self):
        """Prueft Eingaben und Bestaetigungen. False = Start abbrechen."""
        L = self.lang

        if self.dedup.get():
            # Dedup laeuft im Zielordner – Quellen und Filter sind hier ohne
            # Bedeutung.
            if not self.ziel.get():
                messagebox.showwarning(L["msg_missing_title"], L["msg_choose_target"])
                return False
            if not self._dedup_freigabe():
                messagebox.showinfo(
                    L.get("confirm_force_title", "Hinweis"),
                    L.get("hint_dedup_locked", ""),
                )
                return False
            if self.dedup_force.get():
                # Die erweiterte Regel vergleicht den Inhalt nicht – warnen.
                return messagebox.askyesno(
                    L.get("confirm_force_title", "Force mode"),
                    L.get("confirm_force_msg", ""),
                )
            return True

        if not self.q1.get() and not self.q2.get():
            messagebox.showwarning(L["msg_missing_title"], L["msg_choose_source"])
            return False

        if not self.ziel.get():
            messagebox.showwarning(L["msg_missing_title"], L["msg_choose_target"])
            return False

        f1p = [s.strip() for s in self.filter1.get().split(",") if s.strip()]
        f2p = [s.strip() for s in self.filter2.get().split(",") if s.strip()]
        return self._confirm_preview(f1p, f2p)

    def start(self):
        if not self._bestaetige_start():
            return
        L = self.lang

        self._log_clear()
        self.stop_event.clear()
        self._set_status(self.lang.get("status_running", "Laeuft..."))
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.progress["value"] = 0
        self.progress_index["value"] = 0

        self._idx_state = None
        self._sort_state = None
        self._refresh_progress_labels()

        self.start_zeit = datetime.now()
        self.phase_start = datetime.now()
        self._phase_aktiv = None
        self.ende_zeit = None

        f1 = [s.strip() for s in self.filter1.get().split(",") if s.strip()]
        f2 = [s.strip() for s in self.filter2.get().split(",") if s.strip()]

        if self.dedup.get():
            self.sorter = DedupSorter(
                self._dedup_ziel(),
                self.trockenlauf.get(),
                self.dedup_force.get(),
                L,
                self.log_q,
                self.stop_event,
            )
        else:
            gemeinsam = self._aktueller_struct_key == "together"
            ziel_pfad, umgeleitet = self._effektives_ziel()
            self.sorter = Sorter(
                self.q1.get(),
                self.q2.get(),
                f1,
                f2,
                ziel_pfad,
                self.trockenlauf.get(),
                self.skip_existing.get(),
                gemeinsam,
                self._aktueller_gran_key,
                self._aktueller_naming_key,
                L,
                self.log_q,
                self.stop_event,
                ziel_umgeleitet=umgeleitet,
            )
        self.sorter.start()

    def stoppen(self, confirm=True):
        sorter = getattr(self, "sorter", None)
        laeuft = sorter is not None and sorter.is_alive()
        if confirm and laeuft and not self.stop_event.is_set():
            L = self.lang
            if not messagebox.askyesno(
                L.get("confirm_cancel_title", "Cancel"),
                L.get("confirm_cancel_msg", "Stop the current run?"),
            ):
                return
        self.stop_event.set()
        self.btn_stop.config(state="disabled")

    def _refresh_progress_labels(self):
        L = self.lang

        if self._idx_state is None:
            self.lbl_index.config(text=L["lbl_index_default"])
        elif self._idx_state == "empty":
            self.lbl_index.config(text=L["index_empty"])
        elif self._idx_state == "100":
            self.lbl_index.config(text=L["index_100"])
        elif isinstance(self._idx_state, tuple):
            cur, tot = self._idx_state
            pct = cur / tot * 100 if tot else 0
            text = L.get("lbl_index_progress", "{cur}/{tot}  ({pct}%)").format(
                cur=cur, tot=tot, pct=f"{pct:.1f}"
            )
            if self._phase_aktiv == "index" and self.phase_start is not None:
                phase = str(datetime.now() - self.phase_start).split(".")[0]
                text += f"   |   {L['index_time']}: {phase}"
            self.lbl_index.config(text=text)

        if self._sort_state is None:
            base = L["lbl_sort_default"]
        else:
            cur, tot = self._sort_state
            pct = min(100, cur / tot * 100) if tot else 0
            base = L.get("lbl_sort_progress", "{cur}/{tot}  ({pct}%)").format(
                cur=cur, tot=tot, pct=f"{pct:.1f}"
            )

        if self.start_zeit is not None:
            if self.ende_zeit is not None:
                gesamt = str(self.ende_zeit - self.start_zeit).split(".")[0]
            else:
                gesamt = str(datetime.now() - self.start_zeit).split(".")[0]
            base += f"   |   {L['total_time']}: {gesamt}"
        self.lbl_sort.config(text=base)

    def _aktualisiere_zeiten(self):
        self._refresh_progress_labels()
        self.after(1000, self._aktualisiere_zeiten)

    def poll_log(self):
        try:
            while True:
                tag, text = self.log_q.get_nowait()

                if tag == "index":
                    current, total = text
                    if total > 0:
                        self.progress_index["value"] = current / total * 100
                        self._idx_state = (current, total)
                    else:
                        self._idx_state = "empty"
                        self.progress_index["value"] = 0
                    self._refresh_progress_labels()
                    continue

                if tag == "phase":
                    self.phase_start = datetime.now()
                    self._phase_aktiv = text
                    if text == "sort":
                        self._idx_state = "100"
                        self.progress_index["value"] = 100
                    self._refresh_progress_labels()
                    continue

                if tag == "sort_progress":
                    current, total = text
                    if total > 0:
                        self.progress["value"] = min(100, current / total * 100)
                        self._sort_state = (current, total)
                    self._refresh_progress_labels()
                    continue

                if tag == "finished":
                    self.btn_start.config(state="normal")
                    self.btn_stop.config(state="disabled")
                    self.progress["value"] = 100
                    self._phase_aktiv = None
                    self.ende_zeit = datetime.now()
                    self._refresh_progress_labels()
                    self._set_status(self.lang.get("status_ready", "Bereit"))
                    # Nach einem Lauf kann Dedup freigeschaltet sein.
                    self._aktualisiere_dedup_freigabe()
                    self.after(200, self._show_finish_dialog)
                    continue

                self._append_log(text, tag)

        except queue.Empty:
            pass
        self.after(200, self.poll_log)
