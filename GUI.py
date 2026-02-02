import os
import sys
import glob


# --- FIX: MANUALLY FORCE TCL/TK PATHS ---
base_path = r"C:\Users\zeche\AppData\Local\Programs\Python\Python313"

tcl_dir = os.path.join(base_path, "tcl")
tcl_lib = os.path.join(tcl_dir, "tcl8.6")
tk_lib = os.path.join(tcl_dir, "tk8.6")

if os.path.exists(tcl_lib) and os.path.exists(tk_lib):
    os.environ['TCL_LIBRARY'] = tcl_lib
    os.environ['TK_LIBRARY'] = tk_lib
else:
    found_tcl = glob.glob(os.path.join(tcl_dir, "tcl8*"))
    found_tk = glob.glob(os.path.join(tcl_dir, "tk8*"))
    if found_tcl and found_tk:
        os.environ['TCL_LIBRARY'] = found_tcl[0]
        os.environ['TK_LIBRARY'] = found_tk[0]
# --- END FIX ---

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledFrame
import datetime


class LectureRecorderApp(ttk.Window):
    def __init__(self):
        super().__init__(themename = "superhero")
        self.title("NoteCompiler")
        self.geometry("950x750")

        # --- FONT CONFIGURATION (MEDIUM STRENGTH) ---
        # 1. Global default font: Size 11 (Clear, readable)
        self.style.configure('.', font = ('Helvetica', 11))
        # 2. Buttons: Size 11 Bold
        self.style.configure('TButton', font = ('Helvetica', 11, 'bold'))
        # 3. Standard Labels: Size 11
        self.style.configure('TLabel', font = ('Helvetica', 11))

        # State variables
        self.is_recording = False
        self.start_time = None
        self.timer_id = None

        self.container = ttk.Frame(self)
        self.container.pack(fill = BOTH, expand = YES)

        self.show_home()

    def show_home(self):
        self._clear_container()

        # --- Top Section ---
        header_frame = ttk.Frame(self.container, bootstyle = "secondary")
        header_frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.25)

        self.control_frame = ttk.Frame(header_frame, bootstyle = "secondary")
        self.control_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        if not self.is_recording:
            self._draw_record_button()
        else:
            self._draw_timer_display()

        # --- Bottom Section ---
        list_area = ttk.Frame(self.container)
        list_area.place(relx = 0, rely = 0.25, relwidth = 1, relheight = 0.75)

        # Header: Size 16 (Strong, but not huge)
        ttk.Label(
            list_area,
            text = "Recent Recordings",
            font = ("Helvetica", 16, "bold")
        ).pack(fill = X, padx = 20, pady = 15)

        sf = ScrolledFrame(list_area, autohide = True)
        sf.pack(fill = BOTH, expand = YES, padx = 20, pady = (0, 20))

        dummy_data = [
            {"file": "math2b_12-06-26.wav", "date": "Dec 06"},
            {"file": "phys101_12-05-26.wav", "date": "Dec 05"},
            {"file": "cs50_intro_12-04-26.wav", "date": "Dec 04"},
            {"file": "history_civ_12-02-26.wav", "date": "Dec 02"},
            {"file": "bio_lab_11-30-26.wav", "date": "Nov 30"},
        ]

        for item in dummy_data:
            self._create_card(sf, item)

    def _create_card(self, parent, data):
        card = ttk.Frame(parent, bootstyle = "dark", padding = 12)
        card.pack(fill = X, pady = 6)

        # Filename: Size 13 Bold
        lbl = ttk.Label(
            card,
            text = data['file'],
            font = ("Helvetica", 13, "bold"),
            bootstyle = "inverse-dark"
        )
        lbl.pack(side = LEFT, padx = 15)

        btn_frame = ttk.Frame(card, bootstyle = "dark")
        btn_frame.pack(side = RIGHT)

        ttk.Button(
            btn_frame,
            text = "Play Audio",
            bootstyle = "info-outline",
            command = lambda f = data['file']: print(f"Playing {f}...")
        ).pack(side = LEFT, padx = 5)

        ttk.Button(
            btn_frame,
            text = "View Transcription",
            bootstyle = "success",
            command = lambda f = data['file']: self.show_transcription(f)
        ).pack(side = LEFT, padx = 10)

    def _draw_record_button(self):
        for widget in self.control_frame.winfo_children(): widget.destroy()

        self.record_btn = ttk.Button(
            self.control_frame,
            text = "Start Recording",
            bootstyle = "danger",
            width = 18,
            command = self.start_recording,
        )
        # Medium padding
        self.record_btn.pack(ipady = 20)

    def _draw_timer_display(self):
        for widget in self.control_frame.winfo_children(): widget.destroy()

        # Timer: Size 36 (Large/Clear)
        self.timer_label = ttk.Label(
            self.control_frame,
            text = "00:00:00",
            font = ("Helvetica", 36, "bold"),
            bootstyle = "inverse-secondary"
        )
        self.timer_label.pack(side = TOP, pady = 8)

        stop_btn = ttk.Button(
            self.control_frame,
            text = "Stop Recording",
            bootstyle = "warning-outline",
            width = 18,
            command = self.stop_recording
        )
        stop_btn.pack(side = TOP, pady = 8)

    def start_recording(self):
        self.is_recording = True
        self.start_time = datetime.datetime.now()
        self._draw_timer_display()
        self._update_timer()

    def stop_recording(self):
        self.is_recording = False
        if self.timer_id: self.after_cancel(self.timer_id)
        self._draw_record_button()
        print("Recording stopped.")

    def _update_timer(self):
        if self.is_recording:
            now = datetime.datetime.now()
            diff = now - self.start_time
            total_seconds = int(diff.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.config(text = f"{hours:02}:{minutes:02}:{seconds:02}")
            self.timer_id = self.after(1000, self._update_timer)

    def show_transcription(self, filename):
        self._clear_container()

        nav_frame = ttk.Frame(self.container, padding = 12)
        nav_frame.pack(fill = X)

        ttk.Button(nav_frame, text = "← Back to Home", bootstyle = "primary-outline",
                   command = self.show_home).pack(side = LEFT)

        # Title: Size 14 Bold
        ttk.Label(nav_frame, text = filename, font = ("Helvetica", 14, "bold")).pack(side = LEFT,
                                                                                     padx = 20)

        content_frame = ttk.Frame(self.container, padding = 12)
        content_frame.pack(fill = BOTH, expand = YES)
        content_frame.columnconfigure(0, weight = 1)
        content_frame.columnconfigure(1, weight = 1)
        content_frame.rowconfigure(1, weight = 1)

        # Sub-headers: Size 12 Bold
        ttk.Label(content_frame, text = "Full Transcription", font = ("Helvetica", 14, "bold"),
                  bootstyle = "info").grid(row = 0, column = 0, sticky = "w", pady = 8)

        # Body Text: Size 11 (Standard reading size)
        trans_text = ttk.Text(content_frame, height = 20, wrap = WORD, font = ("Helvetica", 12))
        trans_text.grid(row = 1, column = 0, sticky = "nsew", padx = (0, 10))
        trans_text.insert("1.0", "Transcription text placeholder...")

        ttk.Label(content_frame, text = "AI Summary", font = ("Helvetica", 14, "bold"),
                  bootstyle = "success").grid(row = 0, column = 1, sticky = "w", pady = 8)

        sum_text = ttk.Text(content_frame, height = 20, wrap = WORD, font = ("Helvetica", 12))
        sum_text.grid(row = 1, column = 1, sticky = "nsew", padx = (10, 0))
        sum_text.insert("1.0", "Summary text placeholder...")

    def _clear_container(self):
        for widget in self.container.winfo_children(): widget.destroy()

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = LectureRecorderApp()
    app.run()