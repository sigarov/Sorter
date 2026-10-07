"""GUI (App) fuer den Sortierer."""

import os
import queue
import threading
from datetime import datetime

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config import (WINDOW_TITLE, NAMING_OPTIONS, GRAN_OPTIONS, STRUCT_OPTIONS,
                     SORT_UNTERORDNER)
from translations import TRANSLATIONS
from sorter import Sorter
from dedup_sorter import DedupSorter
from help_texts import get_help


LANG_CODES = ["en", "de", "ru", "fr", "es", "pl", "tr"]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.modus_var = tk.StringVar(value="sort")
        self._log_lines = []
        self._log_only_errors = tk.BooleanVar(value=False)
        self._log_autoscroll = tk.BooleanVar(value=True)
        self._log_search = tk.StringVar()
        self.status_text = tk.StringVar(value="")
        self._settings = {}
        self._syncing_mode = False
        self._ui_ready = False
        self.lang_code = "de"
        self.lang = TRANSLATIONS[self.lang_code]

        self.geometry("920x800")
        self.resizable(True, True)
        self.minsize(800, 680)
        self.configure(padx=12, pady=10)

        self.q1 = tk.StringVar()
        self.q2 = tk.StringVar()
        self.ziel = tk.StringVar()
        self.filter1 = tk.StringVar()
        self.filter2 = tk.StringVar()
        self.trockenlauf = tk.BooleanVar(value=False)
        self.skip_existing = tk.BooleanVar(value=False)
        self.dedup = tk.BooleanVar(value=False)
        self.dedup_force = tk.BooleanVar(value=False)
        self.dedup_action = tk.StringVar(value="move")
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

        self._text_widgets = {}

        # ---------- Sprache (oben) ----------
        fr_lang = tk.Frame(self)
        fr_lang.pack(fill="x", pady=(0, 6))
        self._text_widgets["lbl_lang"] = tk.Label(fr_lang, text="", font=("", 10, "bold"))
        self._text_widgets["lbl_lang"].pack(side="left")
        self.cmb_lang = ttk.Combobox(fr_lang, textvariable=self.lang_display,
                                     values=[TRANSLATIONS[c]["name"] for c in LANG_CODES],
                                     state="readonly", width=15)
        self.cmb_lang.pack(side="left", padx=6)
        self.cmb_lang.bind("<<ComboboxSelected>>", self._on_lang_change)

        # ---------- Hauptbereich: 2 Spalten (links Ordner, rechts Optionen) ----------
        fr_main = tk.Frame(self)
        fr_main.pack(fill="x", pady=(0, 6))
        fr_main.columnconfigure(0, weight=1, uniform="col")
        fr_main.columnconfigure(1, weight=1, uniform="col")

        # ================= LINKE SPALTE: Ordner untereinander =================
        left_col = tk.Frame(fr_main)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # --- Laufwerk / Ordner 1 ---
        left1 = tk.Frame(left_col)
        left1.pack(fill="x")
        self._text_widgets["lbl_source1"] = tk.Label(left1, text="", font=("", 10, "bold"))
        self._text_widgets["lbl_source1"].pack(anchor="w")
        fr1 = tk.Frame(left1); fr1.pack(fill="x", pady=(0, 3))
        tk.Entry(fr1, textvariable=self.q1).pack(side="left", fill="x", expand=True)
        self.btn_w1 = tk.Button(fr1, text="", command=lambda: self.waehle(self.q1, "source1"))
        self.btn_w1.pack(side="left", padx=(4, 0))
        self._text_widgets["lbl_filter1"] = tk.Label(left1, text="", fg="#444")
        self._text_widgets["lbl_filter1"].pack(anchor="w")
        tk.Entry(left1, textvariable=self.filter1).pack(fill="x", pady=(0, 1))
        self._text_widgets["lbl_filter_hint1"] = tk.Label(left1, text="", fg="#888", font=("", 8))
        self._text_widgets["lbl_filter_hint1"].pack(anchor="w")

        # --- Laufwerk / Ordner 2 ---
        left2 = tk.Frame(left_col)
        left2.pack(fill="x", pady=(10, 0))
        self._text_widgets["lbl_source2"] = tk.Label(left2, text="", font=("", 10, "bold"))
        self._text_widgets["lbl_source2"].pack(anchor="w")
        fr2 = tk.Frame(left2); fr2.pack(fill="x", pady=(0, 3))
        tk.Entry(fr2, textvariable=self.q2).pack(side="left", fill="x", expand=True)
        self.btn_w2 = tk.Button(fr2, text="", command=lambda: self.waehle(self.q2, "source2"))
        self.btn_w2.pack(side="left", padx=(4, 0))
        self._text_widgets["lbl_filter2"] = tk.Label(left2, text="", fg="#444")
        self._text_widgets["lbl_filter2"].pack(anchor="w")
        tk.Entry(left2, textvariable=self.filter2).pack(fill="x", pady=(0, 1))
        self._text_widgets["lbl_filter_hint2"] = tk.Label(left2, text="", fg="#888", font=("", 8))
        self._text_widgets["lbl_filter_hint2"].pack(anchor="w")

        # --- Ziel (3. Laufwerk) ---
        left3 = tk.Frame(left_col)
        left3.pack(fill="x", pady=(10, 0))
        self._text_widgets["lbl_target"] = tk.Label(left3, text="", font=("", 10, "bold"))
        self._text_widgets["lbl_target"].pack(anchor="w")
        self.ziel_frame = tk.Frame(left3); self.ziel_frame.pack(fill="x", pady=(0, 3))
        self.ziel_entry = tk.Entry(self.ziel_frame, textvariable=self.ziel)
        self.ziel_entry.pack(side="left", fill="x", expand=True)
        self.btn_w3 = tk.Button(self.ziel_frame, text="",
                                command=lambda: self.waehle(self.ziel, "target"))
        self.btn_w3.pack(side="left", padx=(4, 0))

        # --- Start/Stop direkt unter Target (linke Spalte) ---
        btn_box = tk.Frame(left_col)
        btn_box.pack(fill="x", pady=(8, 12))
        self.btn_start = tk.Button(
            btn_box, text="", bg="#2196F3", fg="white",
            activebackground="#1976D2", activeforeground="white",
            font=("", 11, "bold"), relief="raised", bd=2,
            command=self.start)
        self.btn_start.pack(side="left", ipadx=20)
        self.btn_stop = tk.Button(
            btn_box, text="", state="disabled",
            bg="#F44336", fg="white",
            activebackground="#D32F2F", activeforeground="white",
            disabledforeground="#eeeeee",
            font=("", 11, "bold"), relief="raised", bd=2,
            command=self.stoppen)
        self.btn_stop.pack(side="left", padx=8)

        # --- Target-Index & Sortierung (ganz unten links, ueber der punktierten Linie) ---
        idx_box = tk.Frame(left_col)
        self.lbl_index = tk.Label(idx_box, text="", font=("", 9), fg="#555")
        self.lbl_index.pack(anchor="w")
        self.progress_index = ttk.Progressbar(idx_box, mode="determinate")
        self.progress_index.pack(fill="x", pady=(2, 0))

        srt_box = tk.Frame(left_col)
        self.lbl_sort = tk.Label(srt_box, text="", font=("", 9), fg="#555")
        self.lbl_sort.pack(anchor="w")
        self.progress = ttk.Progressbar(srt_box, mode="determinate")
        self.progress.pack(fill="x", pady=(2, 0))

        # von unten her anordnen: Sortierung ganz unten, Ziel-Index darueber
        srt_box.pack(side="bottom", fill="x")
        idx_box.pack(side="bottom", fill="x", pady=(0, 6))


        # ================= RECHTE SPALTE: Optionen in Gruppen =================
        right_col = tk.Frame(fr_main)
        right_col.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # --- Gruppe 1: Allgemein ---
        self.grp_general = tk.LabelFrame(right_col, text="", bd=3,
                                         relief="ridge", padx=8, pady=4,
                                         font=("", 9, "bold"))
        self.grp_general.pack(fill="x", pady=(0, 8))
        self._help_button(self.grp_general, "general")

        self.chk_dry = ttk.Checkbutton(
            self.grp_general, variable=self.trockenlauf, text="")
        self.chk_dry.pack(anchor="w")

        self.chk_skip = ttk.Checkbutton(
            self.grp_general, variable=self.skip_existing, text="")
        self.chk_skip.pack(anchor="w")

        # --- Tabs: modus-spezifische Optionen ---
        self.nb = ttk.Notebook(right_col)
        self.nb.pack(fill="both", expand=True)
        self.tab_sort = tk.Frame(self.nb)
        self.tab_dedup = tk.Frame(self.nb)
        self.nb.add(self.tab_sort, text="")
        self.nb.add(self.tab_dedup, text="")
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

        # --- Gruppe 2: Deduplizierung (Tab "Bereinigen") ---
        self.grp_dedup = tk.LabelFrame(self.tab_dedup, text="", bd=3,
                                       relief="ridge", padx=8, pady=4,
                                       font=("", 9, "bold"))
        self.grp_dedup.pack(fill="both", expand=True, padx=2, pady=2)
        self._help_button(self.grp_dedup, "dedup")

        self.chk_dedup = ttk.Checkbutton(
            self.grp_dedup, variable=self.dedup, text="")

        # Aktionsauswahl (gehoert zum Hauptschalter)
        self._text_widgets["lbl_dedup_action"] = tk.Label(
            self.grp_dedup, text="", font=("", 9, "bold"))
        self._text_widgets["lbl_dedup_action"].pack(
            anchor="w", padx=(20, 0), pady=(8, 2))

        self.rb_dedup_move = ttk.Radiobutton(
            self.grp_dedup, variable=self.dedup_action, value="move",
            command=self._update_dedup_hint, text="")
        self.rb_dedup_move.pack(anchor="w", padx=(40, 0))

        self.rb_dedup_delete = ttk.Radiobutton(
            self.grp_dedup, variable=self.dedup_action, value="delete",
            command=self._update_dedup_hint, text="")
        self.rb_dedup_delete.pack(anchor="w", padx=(40, 0))

        # Trennlinie zur naechsten Regel (Force)
        ttk.Separator(self.grp_dedup, orient="horizontal").pack(
            fill="x", pady=(8, 6))

        # Force-Regel (eigene, unabhaengige Zusatzregel)
        self._text_widgets["lbl_dedup_extra"] = tk.Label(
            self.grp_dedup, text="", font=("", 9, "bold"))
        self._text_widgets["lbl_dedup_extra"].pack(
            anchor="w", pady=(0, 2))

        self.chk_dedup_force = ttk.Checkbutton(
            self.grp_dedup, variable=self.dedup_force, text="")
        self.chk_dedup_force.pack(anchor="w", padx=(0, 0), pady=(0, 4))

        self._text_widgets["lbl_dedup_hint"] = tk.Label(
            self.grp_dedup, text="", fg="#888", font=("", 8),
            justify="left", wraplength=350)
        self._text_widgets["lbl_dedup_hint"].pack(anchor="w", pady=(2, 0))

        # --- Gruppe 3: Sortierung & Namen (Tab "Sortieren") ---
        self.grp_naming = tk.LabelFrame(self.tab_sort, text="", bd=3,
                                        relief="ridge", padx=8, pady=4,
                                        font=("", 9, "bold"))
        self.grp_naming.pack(fill="both", expand=True, padx=2, pady=2)
        self._help_button(self.grp_naming, "naming")

        self._text_widgets["lbl_naming"] = tk.Label(
            self.grp_naming, text="", font=("", 9, "bold"))
        self._text_widgets["lbl_naming"].pack(anchor="w", pady=(0, 2))
        self.cmb_naming = ttk.Combobox(self.grp_naming,
                                       textvariable=self.naming_label,
                                       state="readonly")
        self.cmb_naming.pack(fill="x")
        self.cmb_naming.bind("<<ComboboxSelected>>", self._on_naming_change)
        self._text_widgets["lbl_hint"] = tk.Label(
            self.grp_naming, text="", fg="#888", font=("", 8),
            justify="left", wraplength=350)
        self._text_widgets["lbl_hint"].pack(anchor="w", pady=(2, 6))

        fr_struct = tk.Frame(self.grp_naming)
        fr_struct.pack(fill="x", anchor="w")
        self._text_widgets["lbl_structure"] = tk.Label(
            fr_struct, text="", font=("", 9, "bold"))
        self._text_widgets["lbl_structure"].pack(side="left")
        self.cmb_struct = ttk.Combobox(fr_struct, textvariable=self.struct_label,
                                       state="readonly", width=24)
        self.cmb_struct.pack(side="left", padx=6)
        self.cmb_struct.bind("<<ComboboxSelected>>", self._on_struct_change)

        fr_gran = tk.Frame(self.grp_naming)
        fr_gran.pack(fill="x", anchor="w", pady=(6, 0))
        self._text_widgets["lbl_granularity"] = tk.Label(
            fr_gran, text="", font=("", 9, "bold"))
        self._text_widgets["lbl_granularity"].pack(side="left")
        self.cmb_gran = ttk.Combobox(fr_gran, textvariable=self.gran_label,
                                     state="readonly", width=22)
        self.cmb_gran.pack(side="left", padx=6)
        self.cmb_gran.bind("<<ComboboxSelected>>", self._on_gran_change)

        # ---------- Gestrichelte Trennlinie ----------
        canvas = tk.Canvas(self, height=2, bd=0, highlightthickness=0)
        canvas.pack(fill="x", pady=10)
        canvas.create_line(0, 0, 2000, 0, dash=(4, 4), fill="#888")

        # ---------- Log ----------
        log_head = tk.Frame(self)
        log_head.pack(fill="x")
        self._text_widgets["lbl_log"] = tk.Label(log_head, text="", font=("", 10, "bold"))
        self._text_widgets["lbl_log"].pack(side="left")

        bar = tk.Frame(log_head)
        bar.pack(side="right")
        self.btn_log_clear = tk.Button(bar, text="", command=self._log_clear)
        self.btn_log_clear.pack(side="left")
        self.btn_log_save = tk.Button(bar, text="", command=self._log_save)
        self.btn_log_save.pack(side="left", padx=4)
        self.btn_log_open = tk.Button(bar, text="", command=self._log_open)
        self.btn_log_open.pack(side="left")
        self.chk_log_errors = ttk.Checkbutton(
            bar, text="", variable=self._log_only_errors,
            command=self._toggle_log_filter)
        self.chk_log_errors.pack(side="left", padx=(8, 0))
        self.chk_log_autoscroll = ttk.Checkbutton(
            bar, text="", variable=self._log_autoscroll)
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

        # ---------- Statusleiste ----------
        status = tk.Label(self, textvariable=self.status_text, anchor="w",
                          fg="#333", bd=1, relief="sunken", padx=6)
        status.pack(fill="x", pady=(4, 0))

        self.txt.tag_config("info", foreground="#8ecae6")
        self.txt.tag_config("warn", foreground="#ffb703")
        self.txt.tag_config("error", foreground="#ef476f")
        self.txt.tag_config("report", foreground="#06d6a0")
        self.txt.tag_config("progress", foreground="#cccccc")

        self._apply_language()
        self._on_dedup_toggle()

        self.after(200, self.poll_log)
        self.after(1000, self._aktualisiere_zeiten)

        self._load_settings()
        self._bind_shortcuts()
        self._ui_ready = True
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._set_status(self.lang.get("status_ready", "Bereit"))

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
        L = self.lang
        self.title(WINDOW_TITLE)

        if hasattr(self, "grp_general"):
            self.grp_general.config(text=L.get("lbl_group_general", "General"))
            self.grp_dedup.config(text=L.get("lbl_group_dedup", "Deduplication"))
            self.grp_naming.config(text=L.get("lbl_group_naming", "Sorting & Names"))

        self._text_widgets["lbl_lang"].config(text=L["lang_label"])
        self.lang_display.set(L["name"])

        if self.dedup.get():
            self._text_widgets["lbl_source1"].config(
                text=L.get("lbl_source1_dedup", L["lbl_source1"]))
            self._text_widgets["lbl_source2"].config(
                text=L.get("lbl_source2_dedup", L["lbl_source2"]))
            self._text_widgets["lbl_target"].config(
                text=L.get("lbl_target_dedup", L["lbl_target"]))
        else:
            self._text_widgets["lbl_source1"].config(text=L["lbl_source1"])
            self._text_widgets["lbl_source2"].config(text=L["lbl_source2"])
            self._text_widgets["lbl_target"].config(text=L["lbl_target"])
        self._text_widgets["lbl_filter1"].config(text=L["lbl_filter_short"])
        self._text_widgets["lbl_filter2"].config(text=L["lbl_filter_short"])
        self._text_widgets["lbl_filter_hint1"].config(text=L["lbl_filter_hint"])
        self._text_widgets["lbl_filter_hint2"].config(text=L["lbl_filter_hint"])
        self._text_widgets["lbl_target"].config(text=L["lbl_target"])

        self.btn_w1.config(text=L["btn_choose"])
        self.btn_w2.config(text=L["btn_choose"])
        self.btn_w3.config(text=L["btn_choose"])

        self.chk_dry.config(text=L["chk_dryrun"])
        self.chk_skip.config(text=L["chk_skip_existing"])
        self.chk_dedup.config(text=L["chk_dedup"])
        self.chk_dedup_force.config(text=L.get("chk_dedup_force", ""))
        if hasattr(self, "lbl_dedup_action"):
            self._text_widgets["lbl_dedup_action"].config(
                text=L.get("lbl_dedup_action", "What should happen?"))
        if hasattr(self, "rb_dedup_move"):
            self.rb_dedup_move.config(
                text=L.get("rb_dedup_move", "Move to _Duplikate"))
            self.rb_dedup_delete.config(
                text=L.get("rb_dedup_delete", "Delete permanently"))
        if "lbl_dedup_extra" in self._text_widgets:
            self._text_widgets["lbl_dedup_extra"].config(
                text=L.get("lbl_dedup_extra", "Additional rule:"))
        self._update_dedup_hint()
        self._text_widgets["lbl_dedup_hint"].config(text=L["lbl_dedup_hint"])

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
        self._text_widgets["lbl_hint"].config(
            text=L["hint_text"].format(nodate=L["folder_no_date"]))

        self.btn_start.config(text=L["btn_start"])
        self.btn_stop.config(text=L["btn_stop"])

        self.cmb_naming["values"] = [L[tr_key] for _, tr_key in NAMING_OPTIONS]
        for key, tr_key in NAMING_OPTIONS:
            if key == self._aktueller_naming_key:
                self.naming_label.set(L[tr_key])
                break

        self._text_widgets["lbl_log"].config(text=L["lbl_log"])

        if hasattr(self, "nb"):
            self.nb.tab(0, text=L.get("mode_sort", "Sortieren"))
            self.nb.tab(1, text=L.get("mode_dedup", "Bereinigen"))
        if hasattr(self, "btn_log_clear"):
            self.btn_log_clear.config(text=L.get("btn_log_clear", "Leeren"))
            self.btn_log_save.config(text=L.get("btn_log_save", "Speichern"))
            self.btn_log_open.config(text=L.get("btn_log_open", "Oeffnen"))
            self.chk_log_errors.config(text=L.get("chk_log_errors", "Nur Fehler"))
            self.chk_log_autoscroll.config(text=L.get("chk_log_autoscroll", "Auto-Scroll"))
        if "lbl_log_search" in self._text_widgets:
            self._text_widgets["lbl_log_search"].config(
                text=L.get("lbl_log_search", "Suchen:"))

        self._refresh_progress_labels()

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
        L = self.lang
        if not self.dedup.get():
            self._text_widgets["lbl_dedup_hint"].config(
                text=L.get("lbl_dedup_hint", ""))
            return
        action = self.dedup_action.get() if hasattr(self, "dedup_action") else "move"
        if action == "move":
            txt = L.get("hint_dedup_move", L.get("lbl_dedup_hint", ""))
        else:
            txt = L.get("hint_dedup_delete", L.get("lbl_dedup_hint", ""))
        self._text_widgets["lbl_dedup_hint"].config(text=txt)

    def _on_dedup_toggle(self):
        self.modus_var.set("dedup" if self.dedup.get() else "sort")
        self._sync_tab()
        state = "disabled" if self.dedup.get() else "normal"
        try:
            self.ziel_entry.config(state=state)
            self.btn_w3.config(state=state)
        except tk.TclError:
            pass

        # Radio-Buttons und Force-Checkbox nur bei aktivem Dedup klickbar
        d_state = "normal" if self.dedup.get() else "disabled"
        for wname in ("rb_dedup_move", "rb_dedup_delete", "chk_dedup_force"):
            w = getattr(self, wname, None)
            if w is not None:
                try:
                    w.config(state=d_state)
                except tk.TclError:
                    pass
        self._update_dedup_hint()

        L = self.lang
        if self.dedup.get():
            self._text_widgets["lbl_source1"].config(
                text=L.get("lbl_source1_dedup", L["lbl_source1"]))
            self._text_widgets["lbl_source2"].config(
                text=L.get("lbl_source2_dedup", L["lbl_source2"]))
            self._text_widgets["lbl_target"].config(
                text=L.get("lbl_target_dedup", L["lbl_target"]))
        else:
            self._text_widgets["lbl_source1"].config(text=L["lbl_source1"])
            self._text_widgets["lbl_source2"].config(text=L["lbl_source2"])
            self._text_widgets["lbl_target"].config(text=L["lbl_target"])

    # ---------- Hilfe (?-Buttons) ----------
    def _help_button(self, parent, section):
        """Kleiner ?-Button, der den Hilfetext zum Abschnitt anzeigt."""
        btn = tk.Button(parent, text="?", width=2, font=("", 8, "bold"),
                        relief="flat", bd=0, fg="#2196F3", cursor="hand2",
                        command=lambda s=section: self._zeige_hilfe(s))
        btn.pack(anchor="e")
        return btn

    def _zeige_hilfe(self, section):
        text = get_help(self.lang_code, section)
        if not text:
            text = self.lang.get("lbl_dedup_hint", "")
        messagebox.showinfo(self.lang.get("lbl_group_" + section, "Hilfe"), text)

    # ---------- Modus / Tabs ----------
    def _on_mode_change(self):
        self.dedup.set(self.modus_var.get() == "dedup")
        self._on_dedup_toggle()

    def _on_tab_change(self, event=None):
        if not getattr(self, "_ui_ready", False):
            return
        if getattr(self, "_syncing_mode", False):
            return
        try:
            idx = self.nb.index(self.nb.select())
        except Exception:
            return
        new_dedup = (idx == 1)
        if self.dedup.get() != new_dedup:
            self.dedup.set(new_dedup)
            self._on_dedup_toggle()

    def _sync_tab(self):
        if getattr(self, "_syncing_mode", False):
            return
        nb = getattr(self, "nb", None)
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
        if self._log_autoscroll.get():
            self.txt.see("end")

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
        self._log_lines = []
        try:
            self.txt.delete("1.0", "end")
        except Exception:
            pass

    def _log_save(self):
        p = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("Alle", "*.*")])
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
        p = filedialog.askopenfilename(
            filetypes=[("Text", "*.txt"), ("Alle", "*.*")])
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
        try:
            from config import BILD_EXT, VIDEO_EXT
            exts = BILD_EXT | VIDEO_EXT
        except Exception:
            exts = None
        n = 0
        size = 0
        limit = 20000
        for q in quellen:
            for root, _dirs, files in os.walk(q):
                for fn in files:
                    if exts is not None and os.path.splitext(fn)[1].lower() not in exts:
                        continue
                    n += 1
                    try:
                        size += os.path.getsize(os.path.join(root, fn))
                    except Exception:
                        pass
                    if n >= limit:
                        break
                if n >= limit:
                    break
        if n == 0:
            return True
        mb = size / (1024.0 * 1024.0)
        size_s = "%.2f GB" % (mb / 1024.0) if mb >= 1024 else "%.1f MB" % mb
        n_s = ">%d" % limit if n >= limit else str(n)
        L = self.lang
        tmpl = L.get("preview_msg", "{n} Dateien gefunden ({size}).\n\nJetzt starten?")
        msg = tmpl.format(n=n_s, size=size_s, src=self.q1.get() or "-",
                          dst=self.ziel.get() or "-")
        return messagebox.askokcancel(L.get("preview_title", "Vorschau"), msg)

    def _show_finish_dialog(self):
        try:
            sorter = getattr(self, "sorter", None)
            stat = getattr(sorter, "stat", None) or {}
            L = self.lang
            txt = "\n".join("%s: %s" % (k, v) for k, v in stat.items())
            dlg = tk.Toplevel(self)
            dlg.title(L.get("dlg_finish_title", "Fertig"))
            dlg.transient(self)
            h = max(4, min(16, len(stat) + 1))
            t = tk.Text(dlg, height=h, width=44, bg="#111", fg="#eee",
                        font=("Consolas", 9))
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

            tk.Button(box, text=L.get("btn_open_log", "Log oeffnen"),
                      command=open_log).pack(side="left")
            tk.Button(box, text=L.get("btn_open_folder", "Ordner oeffnen"),
                      command=open_folder).pack(side="left", padx=6)
            tk.Button(box, text=L.get("btn_close", "Schliessen"),
                      command=dlg.destroy).pack(side="right")
        except Exception:
            pass

    def _open_path(self, path):
        try:
            os.startfile(path)
        except Exception:
            try:
                import subprocess
                subprocess.Popen(["explorer", path])
            except Exception:
                pass

    def _remember_paths(self):
        """Merkt sich den zuletzt gewaehlten Pfad je Feld dauerhaft.

        Die Eingabefelder bleiben beim Start leer; gemerkt wird nur,
        was tatsaechlich gewaehlt oder eingetragen wurde."""
        try:
            for key, var in (("q1", self.q1), ("q2", self.q2), ("ziel", self.ziel)):
                val = var.get().strip()
                if val:
                    self._last_paths[key] = val
            self._save_settings()
        except Exception:
            pass

    # ---------- Einstellungen / Shortcuts ----------
    def _settings_path(self):
        base = os.path.join(os.path.expanduser("~"), ".medien_sortierer")
        try:
            os.makedirs(base, exist_ok=True)
        except Exception:
            base = os.path.expanduser("~")
        return os.path.join(base, "settings.json")

    def _load_settings(self):
        import json
        try:
            with open(self._settings_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
        self._settings = data if isinstance(data, dict) else {}
        geo = self._settings.get("geometry")
        if geo:
            try:
                self.geometry(geo)
            except Exception:
                pass
        lc = self._settings.get("lang")
        if lc in TRANSLATIONS:
            self.lang_code = lc
            self.lang = TRANSLATIONS[lc]
            self._apply_language()
        lp = self._settings.get("last_paths")
        if isinstance(lp, dict):
            for key in ("q1", "q2", "ziel"):
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
            pass

    def _on_close(self):
        try:
            self.stop_event.set()
        except Exception:
            pass
        self._remember_paths()
        self._save_settings()
        self.destroy()

    def _bind_shortcuts(self):
        self.bind("<F5>", lambda e: self.start())
        self.bind("<Escape>", lambda e: self.stoppen())
        self.bind("<Control-l>", lambda e: self._log_clear())
        self.bind("<Control-s>", lambda e: self._log_save())

    # ---------- Sonstiges ----------
    def waehle(self, var, key="default"):
        initial = self._last_paths.get(key) or var.get().strip() or None
        try:
            if initial and os.path.isdir(initial):
                p = filedialog.askdirectory(initialdir=initial)
            else:
                p = filedialog.askdirectory()
        except Exception:
            p = filedialog.askdirectory()
        if p:
            var.set(p)
            self._last_paths[key] = p
            self._remember_paths()

    def _effektives_ziel(self):
        """Liefert (ziel, umgeleitet).

        Sind Quelle und Ziel derselbe Ordner, wird in den Unterordner
        'Sort' umgeleitet, damit die unsortierten Quelldateien nicht
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

    def start(self):
        L = self.lang
        if not self.q1.get() and not self.q2.get():
            messagebox.showwarning(L["msg_missing_title"], L["msg_choose_source"])
            return

        if not self.dedup.get():
            if not self.ziel.get():
                messagebox.showwarning(L["msg_missing_title"], L["msg_choose_target"])
                return

        if not self.dedup.get():
            f1p = [s.strip() for s in self.filter1.get().split(",") if s.strip()]
            f2p = [s.strip() for s in self.filter2.get().split(",") if s.strip()]
            if not self._confirm_preview(f1p, f2p):
                return

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
                self.q1.get(), self.q2.get(), f1, f2,
                self.trockenlauf.get(),
                self.dedup_force.get(),
                self.dedup_action.get() == "move",
                L, self.log_q, self.stop_event)
        else:
            gemeinsam = (self._aktueller_struct_key == "together")
            ziel_pfad, umgeleitet = self._effektives_ziel()
            self.sorter = Sorter(
                self.q1.get(), self.q2.get(), f1, f2,
                ziel_pfad,
                self.trockenlauf.get(),
                self.skip_existing.get(),
                gemeinsam,
                self._aktueller_gran_key,
                self._aktueller_naming_key,
                L, self.log_q, self.stop_event,
                ziel_umgeleitet=umgeleitet)
        self.sorter.start()

    def stoppen(self):
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
            text = {
                "de": f"Ziel-Index: {cur}/{tot}  ({pct:.1f}%)",
                "en": f"Target index: {cur}/{tot}  ({pct:.1f}%)",
                "ru": f"Индекс цели: {cur}/{tot}  ({pct:.1f}%)",
                "fr": f"Index cible : {cur}/{tot}  ({pct:.1f}%)",
                "es": f"Índice: {cur}/{tot}  ({pct:.1f}%)",
                "pl": f"Indeks celu: {cur}/{tot}  ({pct:.1f}%)",
                "tr": f"Hedef dizini: {cur}/{tot}  ({pct:.1f}%)",
            }.get(self.lang_code, f"{cur}/{tot} ({pct:.1f}%)")
            if self._phase_aktiv == "index" and self.phase_start is not None:
                phase = str(datetime.now() - self.phase_start).split(".")[0]
                text += f"   |   {L['index_time']}: {phase}"
            self.lbl_index.config(text=text)

        if self._sort_state is None:
            base = L["lbl_sort_default"]
        else:
            cur, tot = self._sort_state
            pct = min(100, cur / tot * 100) if tot else 0
            base = {
                "de": f"Sortierung: {cur}/{tot}  ({pct:.1f}%)",
                "en": f"Sorting: {cur}/{tot}  ({pct:.1f}%)",
                "ru": f"Сортировка: {cur}/{tot}  ({pct:.1f}%)",
                "fr": f"Tri : {cur}/{tot}  ({pct:.1f}%)",
                "es": f"Clasificación: {cur}/{tot}  ({pct:.1f}%)",
                "pl": f"Sortowanie: {cur}/{tot}  ({pct:.1f}%)",
                "tr": f"Sıralama: {cur}/{tot}  ({pct:.1f}%)",
            }.get(self.lang_code, f"{cur}/{tot} ({pct:.1f}%)")

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
                    self.after(200, self._show_finish_dialog)
                    continue

                self._append_log(text, tag)

                if tag == "error":
                    self.btn_start.config(state="normal")
                    self.btn_stop.config(state="disabled")

        except queue.Empty:
            pass
        self.after(200, self.poll_log)
