import tkinter as tk
from tkinter import font, ttk, Menu, messagebox
import pyvisa
import numpy as np
import csv
from datetime import datetime

# Windows 7/2010 era color scheme
BG_MAIN = "#f0f0f0"  # Light gray background
BG_PANEL = "#ffffff"  # White panels
BG_GRADIENT_TOP = "#e8edf2"  # Gradient top
BG_GRADIENT_BOTTOM = "#d5dce3"  # Gradient bottom
BORDER_COLOR = "#b0b0b0"  # Gray border
BORDER_DARK = "#707070"  # Dark border
TEXT_PRIMARY = "#000000"  # Black text
TEXT_SECONDARY = "#555555"  # Dark gray text
ACCENT_CH3 = "#9932cc"  # Purple for CH3 (darker purple)
ACCENT_CH4 = "#00a000"  # Green for CH4
BUTTON_BG = "#e1e1e1"  # Button background
BUTTON_BORDER = "#adadad"  # Button border
TABLE_HEADER = "#f2f2f2"  # Table header
TABLE_ROW_ALT = "#f9f9f9"  # Alternate row color
HIGHLIGHT = "#cce8ff"  # Selection highlight (Windows blue)

# Connect to oscilloscope
rm = pyvisa.ResourceManager()
scope = rm.open_resource('TCPIP0::10.200.22.14::INSTR')
scope.timeout = 30000
scope.clear()

# Configure acquisition
scope.write("ACQ:STOPAFTER CONT")
scope.write("ACQ:MODE HIRES")
scope.write("DATA:ENCdg RIBinary")
scope.write("DATA:WIDTH 2")
record_length = 100000
scope.write("DATA:START 1")
scope.write(f"DATA:STOP {record_length}")
scope.write("ACQ:STATE RUN")


def get_scaled_waveform(channel):
    """Read waveform from channel and scale using Tektronix preamble."""
    scope.write(f"DATA:SOURCE {channel}")
    ymult = float(scope.query("WFMPRE:YMULT?"))
    yzero = float(scope.query("WFMPRE:YZERO?"))
    yoff = float(scope.query("WFMPRE:YOFF?"))
    raw_data = scope.query_binary_values("CURVE? ", datatype='h', is_big_endian=True)
    scaled = (np.array(raw_data) - yoff) * ymult + yzero
    return np.abs(scaled)


# GUI Setup
root = tk.Tk()
root.title("MaxScope v1.0")
root.geometry("380x720")
root.configure(bg=BG_MAIN)
root.resizable(True, True)
root.minsize(360, 650)

try:
    root.iconbitmap("aim.ico")
except:
    pass

# Fonts
title_font = font.Font(family="Segoe UI", size=11, weight="bold")
value_font = font.Font(family="Segoe UI", size=26, weight="bold")
label_font = font.Font(family="Segoe UI", size=9)
small_font = font.Font(family="Segoe UI", size=8)
table_font = font.Font(family="Segoe UI", size=9)


# Create gradient effect for header
def create_gradient_header(parent):
    canvas = tk.Canvas(parent, height=50, bg=BG_GRADIENT_TOP, highlightthickness=0)
    canvas.pack(fill="x")

    # Simple gradient effect with rectangles
    for i in range(50):
        color_ratio = i / 50
        r1, g1, b1 = int(232 * (1 - color_ratio) + 213 * color_ratio), \
            int(237 * (1 - color_ratio) + 220 * color_ratio), \
            int(242 * (1 - color_ratio) + 227 * color_ratio)
        color = f'#{r1:02x}{g1:02x}{b1:02x}'
        canvas.create_rectangle(0, i, 400, i + 1, fill=color, outline=color)

    return canvas


# Main container with border
main_frame = tk.Frame(root, bg=BORDER_COLOR)
main_frame.pack(fill="both", expand=True, padx=0, pady=0)

# Inner container
inner_frame = tk.Frame(main_frame, bg=BG_MAIN)
inner_frame.pack(fill="both", expand=True, padx=1, pady=1)

# Header with gradient
header_canvas = create_gradient_header(inner_frame)

# Title overlay on gradient
title_label = tk.Label(header_canvas, text="MaxScope", font=title_font,
                       fg=TEXT_PRIMARY, bg=BG_GRADIENT_TOP)
title_label.place(x=15, y=10)

version_label = tk.Label(header_canvas, text="Version 1.0", font=small_font,
                         fg=TEXT_SECONDARY, bg=BG_GRADIENT_TOP)
version_label.place(x=15, y=30)

# Status indicator
status_label = tk.Label(header_canvas, text="● Connected", font=small_font,
                        fg=ACCENT_CH4, bg=BG_GRADIENT_TOP)
status_label.place(x=285, y=28)

# Main content area
content_frame = tk.Frame(inner_frame, bg=BG_MAIN)
content_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Channel readings section
readings_frame = tk.Frame(content_frame, bg=BG_PANEL, relief="solid", bd=1, highlightthickness=0)
readings_frame.pack(fill="x", pady=(0, 10))

readings_title_frame = tk.Frame(readings_frame, bg=TABLE_HEADER, height=24)
readings_title_frame.pack(fill="x")
readings_title_frame.pack_propagate(False)

readings_title = tk.Label(readings_title_frame, text="Current Readings", font=label_font,
                          fg=TEXT_PRIMARY, bg=TABLE_HEADER, anchor="w")
readings_title.pack(side="left", padx=8, pady=4)

# CH4 Display
ch4_frame = tk.Frame(readings_frame, bg=BG_PANEL)
ch4_frame.pack(fill="x", padx=15, pady=(15, 8))

ch4_header = tk.Frame(ch4_frame, bg=BG_PANEL)
ch4_header.pack(fill="x")

ch4_icon = tk.Label(ch4_header, text="●", font=("Segoe UI", 12),
                    fg=ACCENT_CH4, bg=BG_PANEL)
ch4_icon.pack(side="left")

ch4_title = tk.Label(ch4_header, text="Channel 4", font=("Segoe UI", 9, "bold"),
                     fg=TEXT_PRIMARY, bg=BG_PANEL)
ch4_title.pack(side="left", padx=(5, 0))

ch4_value_frame = tk.Frame(ch4_frame, bg=BG_PANEL)
ch4_value_frame.pack(pady=(5, 0))

ch4_label = tk.Label(ch4_value_frame, text="--", fg=ACCENT_CH4,
                     bg=BG_PANEL, font=value_font)
ch4_label.pack(side="left")

ch4_unit = tk.Label(ch4_value_frame, text="A", fg=TEXT_SECONDARY,
                    bg=BG_PANEL, font=("Segoe UI", 11))
ch4_unit.pack(side="left", padx=(5, 0), anchor="s", pady=(0, 5))

# Separator line
sep1 = tk.Frame(readings_frame, bg=BORDER_COLOR, height=1)
sep1.pack(fill="x", padx=10, pady=8)

# CH3 Display
ch3_frame = tk.Frame(readings_frame, bg=BG_PANEL)
ch3_frame.pack(fill="x", padx=15, pady=(8, 15))

ch3_header = tk.Frame(ch3_frame, bg=BG_PANEL)
ch3_header.pack(fill="x")

ch3_icon = tk.Label(ch3_header, text="●", font=("Segoe UI", 12),
                    fg=ACCENT_CH3, bg=BG_PANEL)
ch3_icon.pack(side="left")

ch3_title = tk.Label(ch3_header, text="Channel 3", font=("Segoe UI", 9, "bold"),
                     fg=TEXT_PRIMARY, bg=BG_PANEL)
ch3_title.pack(side="left", padx=(5, 0))

ch3_value_frame = tk.Frame(ch3_frame, bg=BG_PANEL)
ch3_value_frame.pack(pady=(5, 0))

ch3_label = tk.Label(ch3_value_frame, text="--", fg=ACCENT_CH3,
                     bg=BG_PANEL, font=value_font)
ch3_label.pack(side="left")

ch3_unit = tk.Label(ch3_value_frame, text="V", fg=TEXT_SECONDARY,
                    bg=BG_PANEL, font=("Segoe UI", 11))
ch3_unit.pack(side="left", padx=(5, 0), anchor="s", pady=(0, 5))

# History section
history_container = tk.Frame(content_frame, bg=BG_PANEL, relief="solid", bd=1)
history_container.pack(fill="both", expand=True, pady=(0, 10))

history_title_frame = tk.Frame(history_container, bg=TABLE_HEADER, height=24)
history_title_frame.pack(fill="x")
history_title_frame.pack_propagate(False)

history_title = tk.Label(history_title_frame, text="Measurement History", font=label_font,
                         fg=TEXT_PRIMARY, bg=TABLE_HEADER, anchor="w")
history_title.pack(side="left", padx=8, pady=4)

history_count = tk.Label(history_title_frame, text="0", font=small_font,
                         fg=TEXT_SECONDARY, bg=TABLE_HEADER, anchor="e")
history_count.pack(side="right", padx=8)

# Table frame
table_frame = tk.Frame(history_container, bg=BG_PANEL)
table_frame.pack(fill="both", expand=True, padx=0, pady=0)

# Style configuration
style = ttk.Style()
style.theme_use("clam")

style.configure("Classic.Treeview",
                background=BG_PANEL,
                fieldbackground=BG_PANEL,
                foreground=TEXT_PRIMARY,
                borderwidth=0,
                rowheight=24,
                relief="flat")

style.configure("Classic.Treeview. Heading",
                background=TABLE_HEADER,
                foreground=TEXT_PRIMARY,
                borderwidth=1,
                relief="raised",
                font=("Segoe UI", 9))

style.map("Classic.Treeview",
          background=[("selected", HIGHLIGHT)],
          foreground=[("selected", TEXT_PRIMARY)])

style.map("Classic.Treeview. Heading",
          background=[("active", "#e5e5e5")])

columns = ("#", "CH4 (A)", "CH3 (V)")
history_table = ttk.Treeview(table_frame, columns=columns, show="headings",
                             style="Classic.Treeview")

history_table.heading("#", text="#")
history_table.heading("CH4 (A)", text="CH4 (A)")
history_table.heading("CH3 (V)", text="CH3 (V)")

history_table.column("#", width=40, anchor="center")
history_table.column("CH4 (A)", width=130, anchor="center")
history_table.column("CH3 (V)", width=130, anchor="center")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=history_table.yview)
history_table.configure(yscroll=scrollbar.set)

history_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Button frame
button_frame = tk.Frame(content_frame, bg=BG_MAIN)
button_frame.pack(fill="x", pady=(0, 5))


class ClassicButton(tk.Canvas):
    def __init__(self, parent, text, command):
        super().__init__(parent, width=150, height=28, bg=BG_MAIN, highlightthickness=0)
        self.command = command
        self.text = text
        self.pressed = False

        self.draw_button(False)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def draw_button(self, pressed):
        self.delete("all")
        if pressed:
            # Pressed state
            self.create_rectangle(0, 0, 150, 28, fill="#d5d5d5", outline=BORDER_DARK, width=1)
            self.create_line(1, 1, 149, 1, fill=BORDER_DARK)
            self.create_line(1, 1, 1, 27, fill=BORDER_DARK)
            self.create_text(76, 15, text=self.text, font=label_font, fill=TEXT_PRIMARY)
        else:
            # Normal state
            self.create_rectangle(0, 0, 150, 28, fill=BUTTON_BG, outline=BORDER_DARK, width=1)
            self.create_line(1, 27, 149, 27, fill=BORDER_DARK)
            self.create_line(149, 1, 149, 27, fill=BORDER_DARK)
            self.create_line(1, 1, 149, 1, fill="#ffffff")
            self.create_line(1, 1, 1, 27, fill="#ffffff")
            self.create_text(75, 14, text=self.text, font=label_font, fill=TEXT_PRIMARY)

    def on_press(self, event):
        self.pressed = True
        self.draw_button(True)

    def on_release(self, event):
        self.pressed = False
        self.draw_button(False)
        if self.command:
            self.command()

    def on_enter(self, event):
        if not self.pressed:
            self.delete("all")
            self.create_rectangle(0, 0, 150, 28, fill="#e5f3ff", outline="#0078d7", width=1)
            self.create_line(1, 27, 149, 27, fill=BORDER_DARK)
            self.create_line(149, 1, 149, 27, fill=BORDER_DARK)
            self.create_line(1, 1, 149, 1, fill="#ffffff")
            self.create_line(1, 1, 1, 27, fill="#ffffff")
            self.create_text(75, 14, text=self.text, font=label_font, fill=TEXT_PRIMARY)

    def on_leave(self, event):
        if not self.pressed:
            self.draw_button(False)


# Button container frame
button_container = tk.Frame(button_frame, bg=BG_MAIN)
button_container.pack(anchor="center")

clear_button = ClassicButton(button_container, "Clear History", command=lambda: clear_history())
clear_button.pack(side="left", padx=5)

export_button = ClassicButton(button_container, "Export to CSV", command=lambda: export_to_csv())
export_button.pack(side="left", padx=5)

# Variables
last_ch3 = None
last_ch4 = None
history = []

# Context Menu
context_menu = tk.Menu(history_table, tearoff=0)
context_menu.add_command(label="Clear Selected", command=lambda: clear_selected())
context_menu.add_separator()
context_menu.add_command(label="Clear All", command=lambda: clear_history())
context_menu.add_separator()
context_menu.add_command(label="Export to CSV", command=lambda: export_to_csv())


def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)
    context_menu.grab_release()


history_table.bind("<Button-3>", show_context_menu)


# Functions
def on_close():
    try:
        scope.write("ACQ:STATE STOP")
    except Exception:
        pass
    try:
        scope.close()
    except Exception:
        pass
    root.destroy()


def refresh_history():
    history_table.delete(*history_table.get_children())
    for i, (ch4_val, ch3_val) in enumerate(history, start=1):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        history_table.insert("", "end", values=(i, f"{ch4_val:.3f}", f"{ch3_val:.3f}"), tags=(tag,))

    history_table.tag_configure("evenrow", background=BG_PANEL)
    history_table.tag_configure("oddrow", background=TABLE_ROW_ALT)

    history_count.config(text=str(len(history)))


def clear_history():
    global history
    history = []
    refresh_history()


def clear_selected():
    selected_items = history_table.selection()
    indices_to_remove = []
    for item in selected_items:
        index = int(history_table.item(item)['values'][0]) - 1
        indices_to_remove.append(index)
        history_table.delete(item)
    indices_to_remove.sort(reverse=True)
    for idx in indices_to_remove:
        if 0 <= idx < len(history):
            del history[idx]
    refresh_history()


def export_to_csv():
    """Export measurement history to CSV file"""
    if not history:
        messagebox.showwarning("No Data", "There is no measurement data to export.")
        return

    try:
        filename = "xscope_data.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['Measurement #', 'CH4 (A)', 'CH3 (V)', 'Timestamp'])
            # Write data with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for i, (ch4_val, ch3_val) in enumerate(history, start=1):
                writer.writerow([i, f"{ch4_val:.3f}", f"{ch3_val:.3f}", timestamp])

        messagebox.showinfo("Export Successful", f"Data exported to {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")


def update_display():
    global last_ch3, last_ch4, history

    try:
        # Read waveforms from both channels
        ch3_values = get_scaled_waveform("CH3")
        ch4_values = get_scaled_waveform("CH4")

        status_label.config(text="● Connected", fg=ACCENT_CH4)

    except Exception as e:
        ch3_label.config(text="ERR", fg="red")
        ch4_label.config(text="ERR", fg="red")
        status_label.config(text="● Error", fg="red")
        root.after(1000, update_display)
        return

    # Find peak in CH4
    peak_index = int(np.argmax(ch4_values))
    peak_ch4 = float(ch4_values[peak_index])
    corresponding_ch3 = float(ch3_values[peak_index])

    # Update display labels
    ch3_label.config(text=f"{corresponding_ch3:.3f}", fg=ACCENT_CH3)
    ch4_label.config(text=f"{peak_ch4:.3f}", fg=ACCENT_CH4)

    # UPDATED: Log when EITHER value changes significantly
    # This captures all changes while preventing duplicate identical readings
    if (
            last_ch3 is None
            or last_ch4 is None
            or abs(corresponding_ch3 - last_ch3) > 0.001
            or abs(peak_ch4 - last_ch4) > 0.001
    ):
        # Additional check: Don't log if BOTH values are identical to last reading
        if last_ch3 is None or last_ch4 is None or not (
                abs(corresponding_ch3 - last_ch3) < 0.001 and abs(peak_ch4 - last_ch4) < 0.001
        ):
            history.append((peak_ch4, corresponding_ch3))
            if len(history) > 100:
                history.pop(0)
            refresh_history()
            # Update last values
            last_ch3, last_ch4 = corresponding_ch3, peak_ch4

    root.after(1000, update_display)


update_display()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()