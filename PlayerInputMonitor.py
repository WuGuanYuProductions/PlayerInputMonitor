import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import threading
import time
from datetime import datetime, timedelta
import pandas as pd
import math
import queue
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageChops
import os
import sys
import re
import platform

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pynput import keyboard, mouse

KEYBOARD_LAYOUT = {
    'Esc': (0, 0, 1.0), 'F1': (0, 2, 1.0), 'F2': (0, 3, 1.0), 'F3': (0, 4, 1.0), 'F4': (0, 5, 1.0),
    'F5': (0, 6.5, 1.0), 'F6': (0, 7.5, 1.0), 'F7': (0, 8.5, 1.0), 'F8': (0, 9.5, 1.0),
    'F9': (0, 11, 1.0), 'F10': (0, 12, 1.0), 'F11': (0, 13, 1.0), 'F12': (0, 14, 1.0),
    '~': (1, 0, 1.0), '1': (1, 1, 1.0), '2': (1, 2, 1.0), '3': (1, 3, 1.0), '4': (1, 4, 1.0), '5': (1, 5, 1.0),
    '6': (1, 6, 1.0), '7': (1, 7, 1.0), '8': (1, 8, 1.0), '9': (1, 9, 1.0), '0': (1, 10, 1.0), '-': (1, 11, 1.0), '=': (1, 12, 1.0), 'Back': (1, 13, 2.0),
    'Tab': (2, 0, 1.5), 'Q': (2, 1.5, 1.0), 'W': (2, 2.5, 1.0), 'E': (2, 3.5, 1.0), 'R': (2, 4.5, 1.0), 'T': (2, 5.5, 1.0),
    'Y': (2, 6.5, 1.0), 'U': (2, 7.5, 1.0), 'I': (2, 8.5, 1.0), 'O': (2, 9.5, 1.0), 'P': (2, 10.5, 1.0), '[': (2, 11.5, 1.0), ']': (2, 12.5, 1.0), '\\': (2, 13.5, 1.5),
    'Caps': (3, 0, 1.8), 'A': (3, 1.8, 1.0), 'S': (3, 2.8, 1.0), 'D': (3, 3.8, 1.0), 'F': (3, 4.8, 1.0), 'G': (3, 5.8, 1.0),
    'H': (3, 6.8, 1.0), 'J': (3, 7.8, 1.0), 'K': (3, 8.8, 1.0), 'L': (3, 9.8, 1.0), ';': (3, 10.8, 1.0), "'": (3, 11.8, 1.0), 'Enter': (3, 12.8, 2.2),
    'LShift': (4, 0, 2.3), 'Z': (4, 2.3, 1.0), 'X': (4, 3.3, 1.0), 'C': (4, 4.3, 1.0), 'V': (4, 5.3, 1.0), 'B': (4, 6.3, 1.0),
    'N': (4, 7.3, 1.0), 'M': (4, 8.3, 1.0), ',': (4, 9.3, 1.0), '.': (4, 10.3, 1.0), '/': (4, 11.3, 1.0), 'RShift': (4, 12.3, 2.7),
    'LCtrl': (5, 0, 1.5), 'LWin': (5, 1.5, 1.25), 'LAlt': (5, 2.75, 1.25), 'Space': (5, 4.0, 6.0), 'RAlt': (5, 10.0, 1.25), 'RWin': (5, 11.25, 1.25), 'RCtrl': (5, 12.5, 1.5)
}

MOUSE_LAYOUT = {
    'LClick': (65, 60, 'rect', 60, 90),
    'RClick': (155, 60, 'rect', 60, 90),
    'MClick': (110, 50, 'rect', 16, 45),
    'ScrollUp': (110, 15, 'circle', 20, 20),
    'ScrollDown': (110, 95, 'circle', 20, 20),
    'Mouse4': (22, 155, 'rect', 14, 40),
    'Mouse5': (22, 215, 'rect', 14, 40)
}

GAMEPAD_BODY_POLY = [
    (150, 70), (200, 75), (250, 80), (300, 75), (350, 70),
    (400, 75), (440, 95), (465, 130), (475, 170),
    (480, 220), (470, 260), (445, 290), (410, 315), (370, 325),
    (345, 295), (310, 240), (250, 235), (190, 240), (155, 295),
    (130, 325), (90, 315), (55, 290), (30, 260), (20, 220),
    (25, 170), (35, 130), (60, 95), (100, 75)
]

GAMEPAD_LAYOUT = {
    'LT': (110, 30, 'rect', 65, 30),
    'RT': (390, 30, 'rect', 65, 30),
    'LB': (120, 65, 'rect', 75, 25),
    'RB': (380, 65, 'rect', 75, 25),
    'LStick': (160, 150, 'circle', 55, 55),
    'RStick': (300, 230, 'circle', 55, 55),
    'D-Pad-Up': (200, 190, 'rect', 26, 26),
    'D-Pad-Down': (200, 242, 'rect', 26, 26),
    'D-Pad-Left': (174, 216, 'rect', 26, 26),
    'D-Pad-Right': (226, 216, 'rect', 26, 26),
    'A': (365, 197, 'circle', 34, 34),
    'B': (407, 155, 'circle', 34, 34),
    'X': (323, 155, 'circle', 34, 34),
    'Y': (365, 113, 'circle', 34, 34),
    'Back': (215, 145, 'circle', 20, 20),
    'Start': (265, 145, 'circle', 20, 20),
}

LUT_R, LUT_G, LUT_B, LUT_A = [], [], [], []
for g in range(256):
    if g == 0:
        LUT_R.append(0); LUT_G.append(0); LUT_B.append(0); LUT_A.append(0)
    elif g < 128:
        t = g / 127.0
        LUT_R.append(int(t * 235))
        LUT_G.append(int(90 + t * 110))
        LUT_B.append(0)
        LUT_A.append(int(25 + t * 110))
    else:
        t = (g - 128) / 127.0
        LUT_R.append(int(235 - t * 25))
        LUT_G.append(int(200 - t * 200))
        LUT_B.append(0)
        LUT_A.append(int(135 + t * 100))

PALETTE_DATA = []
for idx in range(256):
    PALETTE_DATA.extend([LUT_R[idx], LUT_G[idx], LUT_B[idx]])


def get_font(size, is_bold=False):
    sys_type = platform.system()
    paths = []
    if sys_type == "Windows":
        windir = os.environ.get("SystemRoot", "C:\\Windows")
        paths = [
            os.path.join(windir, "Fonts", "msyhbd.ttc" if is_bold else "msyh.ttc"),
            os.path.join(windir, "Fonts", "simhei.ttf"),
            os.path.join(windir, "Fonts", "simsun.ttc")
        ]
    elif sys_type == "Darwin":
        paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/Library/Fonts/Arial Unicode.ttf"
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallback.ttf"
        ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def parse_time_str(s):
    s = s.strip().lower()
    if not s:
        return None
    if ":" in s:
        parts = s.split(":")
        try:
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except ValueError:
            pass
    m_h = re.search(r'(\d+)\s*h', s)
    m_m = re.search(r'(\d+)\s*m', s)
    m_s = re.search(r'(\d+)\s*s', s)
    val = 0
    found = False
    if m_h:
        val += int(m_h.group(1)) * 3600
        found = True
    if m_m:
        val += int(m_m.group(1)) * 60
        found = True
    if m_s:
        val += int(m_s.group(1))
        found = True
    if found:
        return val
    try:
        return int(s)
    except ValueError:
        return None


class TimeRangeDialog(tk.Toplevel):
    def __init__(self, parent, total_duration_sec):
        super().__init__(parent)
        self.title("选择导出时间范围")
        self.configure(bg="#0B0F19")
        self.transient(parent)
        self.grab_set()
        
        self.total_duration_sec = total_duration_sec
        self.result = None
        
        tk.Label(self, text="🕒 选择导出的时间区间", font=('Microsoft YaHei', 12, 'bold'), bg="#0B0F19", fg="#00F0FF").pack(pady=(20, 8), padx=25)
        
        fmt_total = self.format_time(total_duration_sec)
        tk.Label(self, text=f"当前监测总时长: {fmt_total}\n格式支持: 1m30s, 90, 01:30 (两栏留空即全量导出)", font=('Microsoft YaHei', 9), bg="#0B0F19", fg="#94A3B8", justify=tk.CENTER).pack(pady=4, padx=25)
        
        f_inputs = tk.Frame(self, bg="#0B0F19")
        f_inputs.pack(pady=10, padx=25)
        
        tk.Label(f_inputs, text="开始时间:", font=('Microsoft YaHei', 10), bg="#0B0F19", fg="#94A3B8").grid(row=0, col=0, padx=8, pady=5)
        self.ent_start = tk.Entry(f_inputs, bg="#1E293B", fg="#00F0FF", insertbackground="#00F0FF", bd=0, width=15, font=('Consolas', 10))
        self.ent_start.grid(row=0, col=1, padx=5, pady=5)
        
        tk.Label(f_inputs, text="结束时间:", font=('Microsoft YaHei', 10), bg="#0B0F19", fg="#94A3B8").grid(row=1, col=0, padx=8, pady=5)
        self.ent_end = tk.Entry(f_inputs, bg="#1E293B", fg="#00F0FF", insertbackground="#00F0FF", bd=0, width=15, font=('Consolas', 10))
        self.ent_end.grid(row=1, col=1, padx=5, pady=5)
        
        f_btns = tk.Frame(self, bg="#0B0F19")
        f_btns.pack(pady=(10, 20), padx=25)
        
        tk.Button(f_btns, text="全量导出", bg="#1E293B", fg="#94A3B8", relief=tk.FLAT, bd=0, padx=15, pady=6, font=('Microsoft YaHei', 9, 'bold'), command=self.on_all).pack(side=tk.LEFT, padx=12)
        tk.Button(f_btns, text="确认区间", bg="#38BDF8", fg="#0F172A", relief=tk.FLAT, bd=0, padx=15, pady=6, font=('Microsoft YaHei', 9, 'bold'), command=self.on_ok).pack(side=tk.LEFT, padx=12)
        
        self.update_idletasks()
        win_w = self.winfo_reqwidth() + 40
        win_h = self.winfo_reqheight() + 10
        
        if parent and parent.winfo_exists():
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()
            parent_w = parent.winfo_width()
            parent_h = parent.winfo_height()
            x = parent_x + (parent_w - win_w) // 2
            y = parent_y + (parent_h - win_h) // 2
            self.geometry(f"{win_w}x{win_h}+{x}+{y}")
        else:
            self.geometry(f"{win_w}x{win_h}")
        
        self.resizable(False, False)

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h > 0: return f"{h}h{m}m{s}s"
        return f"{m}m{s}s"
        
    def on_all(self):
        self.result = (0, self.total_duration_sec)
        self.destroy()
        
    def on_ok(self):
        start_str = self.ent_start.get().strip()
        end_str = self.ent_end.get().strip()
        
        start_val = 0
        if start_str:
            parsed = parse_time_str(start_str)
            if parsed is None or parsed < 0:
                messagebox.showerror("格式错误", "开始时间格式不正确！", parent=self)
                return
            start_val = parsed
            
        end_val = self.total_duration_sec
        if end_str:
            parsed = parse_time_str(end_str)
            if parsed is None or parsed < 0:
                messagebox.showerror("格式错误", "结束时间格式不正确！", parent=self)
                return
            end_val = parsed
            
        if start_val >= end_val:
            messagebox.showerror("逻辑错误", "开始时间必须小于结束时间！", parent=self)
            return
            
        if start_val > self.total_duration_sec:
            messagebox.showerror("范围错误", "开始时间已超过当前监测总时长！", parent=self)
            return
            
        self.result = (start_val, min(end_val, self.total_duration_sec))
        self.destroy()


class InputTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("玩家按键输入实时监控")
        self.root.geometry("1500x900")
        self.root.configure(bg="#0B0F19")
        self.root.protocol("WM_DELETE_WINDOW", self.on_app_close)
        
        if sys.platform == "win32":
            import ctypes
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppModelID("TianGongYouLin.PlayerInputMonitor")
            except Exception:
                pass
        
        self.load_window_icon()
        
        self.monitor_mode = "keyboard_mouse" 
        self.is_monitoring = False
        self.start_time = None
        self.start_time_seconds = 0.0
        self.total_elapsed_seconds = 0
        self.need_redraw = True 
        
        self.keyboard_counts = {k: 0 for k in KEYBOARD_LAYOUT.keys()}
        self.mouse_counts = {k: 0 for k in MOUSE_LAYOUT.keys()}
        self.gamepad_counts = {k: 0 for k in GAMEPAD_LAYOUT.keys()}
        
        self.keyboard_durations = {k: 0.0 for k in KEYBOARD_LAYOUT.keys()}
        self.mouse_durations = {k: 0.0 for k in MOUSE_LAYOUT.keys()}
        self.gamepad_durations = {k: 0.0 for k in GAMEPAD_LAYOUT.keys()}
        
        self.active_presses = {}
        
        self.all_input_timestamps = []
        self.peak_periods = []
        self.current_peak_segment = None
        self.peak_threshold = 100 
        self.peak_window = None
        self.last_peak_check_time = 0.0
        
        self.keyboard_mappings = {k: "" for k in KEYBOARD_LAYOUT.keys()}
        self.mouse_mappings = {k: "" for k in MOUSE_LAYOUT.keys()}
        self.mouse_mappings.update({"MClick_click": "", "MClick_scroll": ""})
        self.gamepad_mappings = {k: "" for k in GAMEPAD_LAYOUT.keys()}
        self.gamepad_mappings.update({
            "LStick_click": "", "LStick_push": "",
            "RStick_click": "", "RStick_push": ""
        })
        
        self.logs = [] 
        self.freq_history = [] 
        self.current_period_count = 0 
        self.last_period_time = time.time()
        
        self.event_queue = queue.Queue()
        self.log_queue = queue.Queue()
        self.cloud_cache = {}
        
        self.kb_listener = None
        self.mouse_listener = None
        self.gp_thread = None
        self.stop_gp_event = threading.Event()
        
        self.kb_photo = None
        self.ms_photo = None
        self.gp_photo = None
        
        self.kb_scale_info = {}
        self.ms_scale_info = {}
        self.gp_scale_info = {}
        
        self.setup_ui()
        self.update_loop()

    def load_window_icon(self):
        base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
        paths = [
            os.path.join(base_dir, "dist", "Resources", "Icon.png"),
            os.path.join(base_dir, "Resources", "Icon.png"),
            os.path.join(base_dir, "..", "dist", "Resources", "Icon.png"),
            "dist/Resources/Icon.png",
            "Resources/Icon.png"
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    img = ImageTk.PhotoImage(file=p)
                    self.root.iconphoto(True, img)
                    self._taskbar_icon_ref = img
                    break
                except Exception:
                    pass

    def get_dpi_scale(self):
        try:
            return self.root.winfo_fpixels('1i') / 72.0
        except Exception:
            return 1.0

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Flat.TButton', font=('Microsoft YaHei', 10, 'bold'), background='#1E293B', foreground='#00F0FF', borderwidth=0)
        style.map('Flat.TButton', background=[('active', '#0F172A'), ('disabled', '#0F172A')], foreground=[('active', '#38BDF8'), ('disabled', '#475569')])
        style.configure('Dark.TSpinbox', background='#1E293B', foreground='#00F0FF', arrowcolor='#00F0FF', borderwidth=0)
        style.configure('Dark.TCombobox', fieldbackground='#1E293B', background='#1E293B', foreground='#00F0FF', arrowcolor='#00F0FF', borderwidth=0)

        ctrl_frame = tk.Frame(self.root, bg="#0F172A", height=80, bd=0)
        ctrl_frame.pack(fill=tk.X, side=tk.TOP, padx=0, pady=0)
        
        self.mode_frame = tk.Frame(ctrl_frame, bg="#0F172A")
        self.mode_frame.pack(side=tk.LEFT, padx=15, pady=15)
        
        self.btn_mode_km = tk.Button(self.mode_frame, text="⌨ 键鼠监测模式", font=('Microsoft YaHei', 10, 'bold'), bg="#38BDF8", fg="#0F172A", relief=tk.FLAT, bd=0, padx=12, pady=6, command=lambda: self.switch_mode("keyboard_mouse"))
        self.btn_mode_km.pack(side=tk.LEFT, padx=4)
        
        self.btn_mode_gp = tk.Button(self.mode_frame, text="🎮 手柄监测模式", font=('Microsoft YaHei', 10, 'bold'), bg="#1E293B", fg="#94A3B8", relief=tk.FLAT, bd=0, padx=12, pady=6, command=lambda: self.switch_mode("gamepad"))
        self.btn_mode_gp.pack(side=tk.LEFT, padx=4)
        
        btn_frame = tk.Frame(ctrl_frame, bg="#0F172A")
        btn_frame.pack(side=tk.LEFT, padx=10, pady=15)
        
        self.btn_monitor = ttk.Button(btn_frame, text="▶ 开始监测", command=self.toggle_monitoring, width=12, style='Flat.TButton')
        self.btn_monitor.pack(side=tk.LEFT, padx=5)
        
        self.btn_clear = ttk.Button(btn_frame, text="🧹 清空记录", command=self.clear_records, width=12, style='Flat.TButton')
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        
        self.btn_export_img = ttk.Button(btn_frame, text="🖼 导出热力图", command=self.export_heatmap, state=tk.DISABLED, width=12, style='Flat.TButton')
        self.btn_export_img.pack(side=tk.LEFT, padx=5)
        
        self.btn_export_csv = ttk.Button(btn_frame, text="📊 导出数据表", command=self.export_log, state=tk.DISABLED, width=12, style='Flat.TButton')
        self.btn_export_csv.pack(side=tk.LEFT, padx=5)

        self.btn_peak_chart = ttk.Button(btn_frame, text="📈 尖峰统计图", command=self.open_peak_chart_window, state=tk.DISABLED, width=12, style='Flat.TButton')
        self.btn_peak_chart.pack(side=tk.LEFT, padx=5)

        status_frame = tk.Frame(ctrl_frame, bg="#0F172A")
        status_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(status_frame, text="热力饱和值:", font=('Microsoft YaHei', 10, 'bold'), bg="#0F172A", fg="#94A3B8").pack(side=tk.LEFT, padx=5)
        self.var_saturation = tk.IntVar(value=100)
        self.spin_saturation = ttk.Spinbox(status_frame, from_=10, to=10000, increment=50, textvariable=self.var_saturation, width=6, font=('Consolas', 10, 'bold'), style='Dark.TSpinbox', command=self.on_saturation_changed)
        self.spin_saturation.pack(side=tk.LEFT, padx=5)
        self.spin_saturation.bind("<Return>", lambda e: self.on_saturation_changed())
        
        self.lbl_status_led = tk.Label(status_frame, text="● IDLE", font=('Microsoft YaHei', 11, 'bold'), bg="#0F172A", fg="#64748B")
        self.lbl_status_led.pack(side=tk.LEFT, padx=10)

        self.lbl_key_counts = tk.Label(status_frame, text="捕获输入: 0 次", font=('Microsoft YaHei', 10, 'bold'), bg="#0F172A", fg="#38BDF8")
        self.lbl_key_counts.pack(side=tk.LEFT, padx=10)

        self.lbl_timer = tk.Label(status_frame, text="⏱ 00:00:00", bg="#1E293B", fg="#F1F5F9", font=('Consolas', 13, 'bold'), padx=10, pady=4)
        self.lbl_timer.pack(side=tk.LEFT, padx=5)

        self.main_frame = tk.Frame(self.root, bg="#0B0F19")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.km_panel_frame = tk.Frame(self.main_frame, bg="#0B0F19")
        self.km_panel_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        kb_container = tk.Frame(self.km_panel_frame, bg="#1E293B", bd=1, relief=tk.FLAT)
        kb_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        kb_title_bar = tk.Frame(kb_container, bg="#111827", height=30)
        kb_title_bar.pack(fill=tk.X)
        tk.Label(kb_title_bar, text="⌨ 键盘热力流动层 (可点击配置映射描述)", bg="#111827", fg="#94A3B8", font=('Microsoft YaHei', 9, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.kb_canvas = tk.Canvas(kb_container, bg="#0F172A", highlightthickness=0)
        self.kb_canvas.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.kb_canvas.bind("<Button-1>", self.on_keyboard_click)

        ms_container = tk.Frame(self.km_panel_frame, bg="#1E293B", bd=1, relief=tk.FLAT, width=280)
        ms_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        ms_container.pack_propagate(False)
        
        ms_title_bar = tk.Frame(ms_container, bg="#111827", height=30)
        ms_title_bar.pack(fill=tk.X)
        tk.Label(ms_title_bar, text="🖱 鼠标热力流动层 (可点击配置)", bg="#111827", fg="#94A3B8", font=('Microsoft YaHei', 9, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.ms_canvas = tk.Canvas(ms_container, bg="#0F172A", highlightthickness=0)
        self.ms_canvas.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.ms_canvas.bind("<Button-1>", self.on_mouse_click)

        self.gp_panel_frame = tk.Frame(self.main_frame, bg="#0B0F19")
        
        gp_container = tk.Frame(self.gp_panel_frame, bg="#1E293B", bd=1, relief=tk.FLAT)
        gp_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        gp_title_bar = tk.Frame(gp_container, bg="#111827", height=30)
        gp_title_bar.pack(fill=tk.X)
        tk.Label(gp_title_bar, text="🎮 手柄热力流动层", bg="#111827", fg="#94A3B8", font=('Microsoft YaHei', 9, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.gp_canvas = tk.Canvas(gp_container, bg="#0F172A", highlightthickness=0)
        self.gp_canvas.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.gp_canvas.bind("<Button-1>", self.on_gamepad_click)

        log_container = tk.Frame(self.main_frame, bg="#1E293B", bd=1, relief=tk.FLAT, width=320)
        log_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=8, pady=5)
        log_container.pack_propagate(False)
        
        log_title_bar = tk.Frame(log_container, bg="#111827", height=30)
        log_title_bar.pack(fill=tk.X)
        tk.Label(log_title_bar, text="📜 操作实时流动日志", bg="#111827", fg="#00F0FF", font=('Microsoft YaHei', 9, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.txt_log = tk.Text(log_container, bg="#0F172A", fg="#38BDF8", bd=0, font=('Consolas', 10), highlightthickness=0)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.lbl_watermark = tk.Label(self.root, text="天工游麟工作室出品", font=('Microsoft YaHei', 9, 'bold'), bg="#0B0F19", fg="#FFFFFF")
        self.lbl_watermark.pack(side=tk.BOTTOM, pady=(5, 10))

        chart_container = tk.Frame(self.root, bg="#1E293B", bd=1, relief=tk.FLAT, height=130)
        chart_container.pack(fill=tk.X, side=tk.BOTTOM, padx=23, pady=(5, 0))
        chart_container.pack_propagate(False)

        chart_title_bar = tk.Frame(chart_container, bg="#111827", height=30)
        chart_title_bar.pack(fill=tk.X)
        
        tk.Label(chart_title_bar, text="📊 玩家操作实时频次波动层", bg="#111827", fg="#94A3B8", font=('Microsoft YaHei', 9, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.freq_unit_var = tk.StringVar(value="每秒 (APS)")
        self.combo_unit = ttk.Combobox(chart_title_bar, values=["每秒 (APS)", "每分 (APM)"], textvariable=self.freq_unit_var, state="readonly", width=12, font=('Microsoft YaHei', 8, 'bold'))
        self.combo_unit.pack(side=tk.LEFT, padx=10)
        self.combo_unit.bind("<<ComboboxSelected>>", self.on_freq_unit_changed)
        
        self.lbl_speed_val = tk.Label(chart_title_bar, text="实时速度: 0 次/秒", bg="#111827", fg="#00F0FF", font=('Microsoft YaHei', 9, 'bold'))
        self.lbl_speed_val.pack(side=tk.RIGHT, padx=15)

        self.chart_canvas = tk.Canvas(chart_container, bg="#0F172A", highlightthickness=0)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.kb_canvas.bind("<Configure>", lambda e: self.trigger_redraw())
        self.ms_canvas.bind("<Configure>", lambda e: self.trigger_redraw())
        self.gp_canvas.bind("<Configure>", lambda e: self.trigger_redraw())
        self.chart_canvas.bind("<Configure>", lambda e: self.draw_frequency_chart())

    def trigger_redraw(self):
        self.need_redraw = True

    def switch_mode(self, mode):
        if self.is_monitoring:
            messagebox.showwarning("警告", "正在监测中，请先停止监测再切换模式！")
            return
        
        self.monitor_mode = mode
        if mode == "keyboard_mouse":
            self.btn_mode_km.config(bg="#38BDF8", fg="#0F172A")
            self.btn_mode_gp.config(bg="#1E293B", fg="#94A3B8")
            self.gp_panel_frame.pack_forget()
            self.km_panel_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:
            self.btn_mode_km.config(bg="#1E293B", fg="#94A3B8")
            self.btn_mode_gp.config(bg="#38BDF8", fg="#0F172A")
            self.km_panel_frame.pack_forget()
            self.gp_panel_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.trigger_redraw()

    def clear_records(self):
        if messagebox.askyesno("确认清空", "您确定要清空当前所有捕获的按键热力记录与日志数据吗？"):
            self.keyboard_counts = {k: 0 for k in KEYBOARD_LAYOUT.keys()}
            self.mouse_counts = {k: 0 for k in MOUSE_LAYOUT.keys()}
            self.gamepad_counts = {k: 0 for k in GAMEPAD_LAYOUT.keys()}
            
            self.keyboard_durations = {k: 0.0 for k in KEYBOARD_LAYOUT.keys()}
            self.mouse_durations = {k: 0.0 for k in MOUSE_LAYOUT.keys()}
            self.gamepad_durations = {k: 0.0 for k in GAMEPAD_LAYOUT.keys()}
            
            self.active_presses.clear()
            self.logs.clear()
            self.freq_history.clear()
            self.current_period_count = 0
            self.all_input_timestamps.clear()
            self.peak_periods.clear()
            self.current_peak_segment = None
            
            self.txt_log.delete("1.0", tk.END)
            self.lbl_key_counts.config(text="捕获输入: 0 次")
            self.lbl_speed_val.config(text=f"实时速度: 0 次/{'秒' if '秒' in self.freq_unit_var.get() else '分'}")
            
            if self.peak_window and self.peak_window.winfo_exists():
                self.peak_window.draw_chart()

            self.trigger_redraw()
            self.draw_frequency_chart()
            messagebox.showinfo("成功", "所有热力数据、按压时长、尖峰波段和历史日志已成功重置！")

    def on_freq_unit_changed(self, event=None):
        self.freq_history.clear()
        self.current_period_count = 0
        self.last_period_time = time.time()
        self.draw_frequency_chart()

    def on_saturation_changed(self, event=None):
        self.trigger_redraw()

    def on_keyboard_click(self, event):
        x, y = event.x, event.y
        unit_w = self.kb_scale_info.get('unit_w', 0)
        unit_h = self.kb_scale_info.get('unit_h', 0)
        start_x = self.kb_scale_info.get('start_x', 0)
        start_y = self.kb_scale_info.get('start_y', 0)
        if unit_w == 0 or unit_h == 0: return

        for key, info in KEYBOARD_LAYOUT.items():
            row, col, kw = info
            kx = start_x + col * unit_w
            ky = start_y + row * unit_h
            kw_px = kw * unit_w - 4
            kh_px = unit_h - 4
            if kx <= x <= kx + kw_px and ky <= y <= ky + kh_px:
                self.prompt_mapping_dialog('keyboard', key)
                break

    def on_mouse_click(self, event):
        x, y = event.x, event.y
        scale = self.ms_scale_info.get('scale', 0)
        offset_x = self.ms_scale_info.get('offset_x', 0)
        offset_y = self.ms_scale_info.get('offset_y', 0)
        if scale == 0: return

        for btn, info in MOUSE_LAYOUT.items():
            bx, by, shape, bw, bh = info
            px = offset_x + bx * scale
            py = offset_y + by * scale
            pw, ph = bw * scale, bh * scale
            
            is_inside = False
            if shape == 'circle':
                dist = math.sqrt((x - px)**2 + (y - py)**2)
                if dist <= pw/2: is_inside = True
            else:
                if px - pw/2 <= x <= px + pw/2 and py - ph/2 <= y <= py + ph/2:
                    is_inside = True
            
            if is_inside:
                self.prompt_mapping_dialog('mouse', btn)
                break

    def on_gamepad_click(self, event):
        x, y = event.x, event.y
        scale = self.gp_scale_info.get('scale', 0)
        offset_x = self.gp_scale_info.get('offset_x', 0)
        offset_y = self.gp_scale_info.get('offset_y', 0)
        if scale == 0: return

        for btn, info in GAMEPAD_LAYOUT.items():
            bx, by, shape, bw, bh = info
            px = offset_x + bx * scale
            py = offset_y + by * scale
            pw, ph = bw * scale, bh * scale
            
            is_inside = False
            if shape == 'circle':
                dist = math.sqrt((x - px)**2 + (y - py)**2)
                if dist <= pw/2: is_inside = True
            else:
                if px - pw/2 <= x <= px + pw/2 and py - ph/2 <= y <= py + ph/2:
                    is_inside = True
            
            if is_inside:
                self.prompt_mapping_dialog('gamepad', btn)
                break

    def prompt_mapping_dialog(self, device, name):
        if device == 'keyboard':
            old_desc = self.keyboard_mappings[name]
            desc = simpledialog.askstring("功能映射配置", f"为 【{name}】 设置功能描述:\n(例如: 闪避 / 普攻 / 视口移动)", initialvalue=old_desc, parent=self.root)
            if desc is not None:
                self.keyboard_mappings[name] = desc.strip()
                self.trigger_redraw()
        elif device == 'mouse':
            if name == 'MClick':
                desc_click = simpledialog.askstring("中键按压配置", f"为 【{name} 按压】 设置功能描述:\n(例如: 锁定目标 / 激活元素)", initialvalue=self.mouse_mappings.get("MClick_click", ""), parent=self.root)
                desc_scroll = simpledialog.askstring("中键滑动配置", f"为 【{name} 滑动】 设置功能描述:\n(例如: 切换武器 / 缩放视角)", initialvalue=self.mouse_mappings.get("MClick_scroll", ""), parent=self.root)
                if desc_click is not None:
                    self.mouse_mappings["MClick_click"] = desc_click.strip()
                if desc_scroll is not None:
                    self.mouse_mappings["MClick_scroll"] = desc_scroll.strip()
                self.trigger_redraw()
            else:
                old_desc = self.mouse_mappings[name]
                desc = simpledialog.askstring("功能映射配置", f"为 【{name}】 设置功能描述:\n(例如: 闪避 / 普攻 / 视口移动)", initialvalue=old_desc, parent=self.root)
                if desc is not None:
                    self.mouse_mappings[name] = desc.strip()
                    self.trigger_redraw()
        elif device == 'gamepad':
            if name in ('LStick', 'RStick'):
                desc_click = simpledialog.askstring(f"{name}按压配置", f"为 【{name} 按压 (L3/R3)】 设置功能描述:\n(例如: 疾跑 / 蹲下)", initialvalue=self.gamepad_mappings.get(f"{name}_click", ""), parent=self.root)
                desc_push = simpledialog.askstring(f"{name}推动配置", f"为 【{name} 推动】 设置功能描述:\n(例如: 角色移动 / 视角移动)", initialvalue=self.gamepad_mappings.get(f"{name}_push", ""), parent=self.root)
                if desc_click is not None:
                    self.gamepad_mappings[f"{name}_click"] = desc_click.strip()
                if desc_push is not None:
                    self.gamepad_mappings[f"{name}_push"] = desc_push.strip()
                self.trigger_redraw()
            else:
                old_desc = self.gamepad_mappings[name]
                desc = simpledialog.askstring("功能映射配置", f"为 【{name}】 设置功能描述:\n(例如: 闪避 / 普攻 / 视口移动)", initialvalue=old_desc, parent=self.root)
                if desc is not None:
                    self.gamepad_mappings[name] = desc.strip()
                    self.trigger_redraw()

    def get_heat_intensity(self, count):
        if count <= 0: return 0.0
        sat_val = max(10, self.var_saturation.get())
        val = math.log1p(count) / math.log1p(sat_val)
        return min(max(val, 0.1), 1.0)

    def draw_radial_cloud(self, img_gray, cx, cy, radius, intensity):
        if intensity <= 0 or radius <= 0: return
        r_int = int(radius)
        intens_key = round(intensity, 2)
        key = (r_int, intens_key)
        
        if key in self.cloud_cache:
            temp_layer = self.cloud_cache[key]
        else:
            size = r_int * 2
            temp_layer = Image.new("L", (size, size), 0)
            draw = ImageDraw.Draw(temp_layer)
            for r in range(r_int, 0, -2):
                factor = (1.0 - r / r_int) ** 1.8
                alpha = int(intensity * 255 * factor)
                draw.ellipse([r_int - r, r_int - r, r_int + r, r_int + r], fill=alpha)
            if len(self.cloud_cache) > 200:
                self.cloud_cache.clear()
            self.cloud_cache[key] = temp_layer
        
        crop_box = (int(cx - r_int), int(cy - r_int), int(cx + r_int), int(cy + r_int))
        img_gray.paste(ImageChops.screen(img_gray.crop(crop_box), temp_layer), (int(cx - r_int), int(cy - r_int)))

    def apply_lut_color(self, img_gray):
        img_p = img_gray.copy()
        img_p.putpalette(PALETTE_DATA)
        img_rgb = img_p.convert("RGB")
        alpha_channel = img_gray.point(lambda p: LUT_A[p])
        return Image.merge("RGBA", (
            img_rgb.getchannel('R'),
            img_rgb.getchannel('G'),
            img_rgb.getchannel('B'),
            alpha_channel
        ))

    def get_adaptive_font_size_multiline(self, base_size_val, text, box_w, box_h, min_sz=5):
        dpi_scale = self.get_dpi_scale()
        base_font_size = max(min_sz, int(base_size_val * dpi_scale))
        
        if not text:
            return base_font_size
        
        lines = text.split('\n')
        max_len = max(len(line) for line in lines)
        
        estimated_width = max_len * (base_font_size * 0.5)
        estimated_height = len(lines) * base_font_size * 1.1
        
        size_by_w = base_font_size
        if estimated_width > (box_w * 0.85):
            size_by_w = int((box_w * 0.85) / (max_len * 0.5))
        
        size_by_h = base_font_size
        if estimated_height > (box_h * 0.85):
            size_by_h = int((box_h * 0.85) / (len(lines) * 1.1))
        
        final_size = min(base_font_size, size_by_w, size_by_h)
        return int(max(min_sz, final_size))

    def get_freq_color(self, val, max_val):
        if max_val <= 0: return "#00FFC2"
        ratio = val / max_val
        if ratio < 0.5:
            t = ratio * 2
            r, g, b = int(t * 230), int(255 - t * 55), int(194 - t * 194)
        else:
            t = (ratio - 0.5) * 2
            r, g, b = int(230 + t * 25), int(200 - t * 150), 0
        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_frequency_chart(self):
        self.chart_canvas.delete("all")
        w = self.chart_canvas.winfo_width()
        h = self.chart_canvas.winfo_height()
        if w < 20 or h < 10: return

        for i in range(1, 4):
            y_pos = h * (i / 4)
            self.chart_canvas.create_line(0, y_pos, w, y_pos, fill="#1B2230", dash=(4, 4))

        if not self.freq_history:
            self.chart_canvas.create_text(w/2, h/2, text="等待玩家操作数据注入...", fill="#64748B", font=('Microsoft YaHei', 9, 'bold'))
            return

        max_limit = 10 if "秒" in self.freq_unit_var.get() else 200
        max_val = max(max(self.freq_history, default=0), max_limit)

        total_bars = 45 
        while len(self.freq_history) > total_bars:
            self.freq_history.pop(0)

        col_w = w / total_bars
        for idx, val in enumerate(self.freq_history):
            bar_h = (val / max_val) * (h - 15)
            x1 = idx * col_w + 3
            y1 = h - bar_h - 2
            x2 = (idx + 1) * col_w - 3
            y2 = h - 2
            
            color = self.get_freq_color(val, max_val)
            self.chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)
            
            if val > 0:
                self.chart_canvas.create_text((x1+x2)/2, y1 - 8, text=str(val), fill="#94A3B8", font=('Consolas', 7))

    def redraw_all(self):
        if self.monitor_mode == "keyboard_mouse":
            self.draw_keyboard_canvas()
            self.draw_mouse_canvas()
        else:
            self.draw_gamepad_canvas()

    def generate_and_bind_heatmap(self, canvas, gray_layer, photo_attr_name):
        colored_heat_img = self.apply_lut_color(gray_layer)
        photo = ImageTk.PhotoImage(colored_heat_img)
        setattr(self, photo_attr_name, photo)
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    def draw_keyboard_canvas(self):
        self.kb_canvas.delete("all")
        w = self.kb_canvas.winfo_width()
        h = self.kb_canvas.winfo_height()
        if w < 20 or h < 20: return

        unit_w, unit_h = w / 16, h / 7
        start_x, start_y = unit_w / 2, unit_h / 2
        self.kb_scale_info = {'unit_w': unit_w, 'unit_h': unit_h, 'start_x': start_x, 'start_y': start_y}

        for key, info in KEYBOARD_LAYOUT.items():
            row, col, kw = info
            kx = start_x + col * unit_w
            ky = start_y + row * unit_h
            self.kb_canvas.create_rectangle(kx, ky, kx + (kw * unit_w - 4), ky + (unit_h - 4), fill="#1B2230", outline="#2F3B52", width=1)

        gray_layer = Image.new("L", (w, h), 0)
        for key, info in KEYBOARD_LAYOUT.items():
            row, col, kw = info
            count = self.keyboard_counts.get(key, 0)
            if count > 0:
                kx = start_x + col * unit_w
                ky = start_y + row * unit_h
                kw_px, kh_px = kw * unit_w - 4, unit_h - 4
                self.draw_radial_cloud(gray_layer, kx + kw_px / 2, ky + kh_px / 2, max(kw_px, kh_px) * 1.3, self.get_heat_intensity(count))

        self.generate_and_bind_heatmap(self.kb_canvas, gray_layer, 'kb_photo')

        for key, info in KEYBOARD_LAYOUT.items():
            row, col, kw = info
            kx = start_x + col * unit_w
            ky = start_y + row * unit_h
            kw_px, kh_px = kw * unit_w - 4, unit_h - 4
            
            count = self.keyboard_counts.get(key, 0)
            mapping = self.keyboard_mappings.get(key, "")

            text_color = "#38BDF8" if count > 0 else "#64748B"
            title_text = f"{key} ({count})"
            font_size = self.get_adaptive_font_size_multiline(unit_h * 0.11, title_text, kw_px, kh_px)
            
            self.kb_canvas.create_text(
                kx + kw_px/2, ky + kh_px/2 - 4 if mapping else ky + kh_px/2, 
                text=title_text, 
                fill=text_color, font=('Microsoft YaHei', font_size, 'bold'), justify=tk.CENTER
            )
            if mapping:
                m_font_size = self.get_adaptive_font_size_multiline(unit_h * 0.08, mapping, kw_px, kh_px)
                self.kb_canvas.create_text(
                    kx + kw_px/2, ky + kh_px - 6, 
                    text=mapping, fill="#00FFC2", font=('Microsoft YaHei', m_font_size, 'normal')
                )

    def draw_mouse_canvas(self):
        self.ms_canvas.delete("all")
        w = self.ms_canvas.winfo_width()
        h = self.ms_canvas.winfo_height()
        if w < 20 or h < 20: return

        scale = min(w / 220, h / 350)
        offset_x = (w - 220 * scale) / 2
        offset_y = (h - 350 * scale) / 2
        
        self.ms_scale_info = {'scale': scale, 'offset_x': offset_x, 'offset_y': offset_y}

        self.ms_canvas.create_oval(offset_x + 20*scale, offset_y + 10*scale, offset_x + 200*scale, offset_y + 340*scale, outline="#2F3B52", width=3)
        for btn, info in MOUSE_LAYOUT.items():
            bx, by, shape, bw, bh = info
            px, py = offset_x + bx * scale, offset_y + by * scale
            pw, ph = bw * scale, bh * scale
            if shape == 'circle':
                self.ms_canvas.create_oval(px - pw/2, py - ph/2, px + pw/2, py + ph/2, fill="#1B2230", outline="#2F3B52", width=1)
            else:
                self.ms_canvas.create_rectangle(px - pw/2, py - ph/2, px + pw/2, py + ph/2, fill="#1B2230", outline="#2F3B52", width=1)

        gray_layer = Image.new("L", (w, h), 0)
        for btn, info in MOUSE_LAYOUT.items():
            bx, by, shape, bw, bh = info
            count = self.mouse_counts.get(btn, 0)
            if count > 0:
                px, py = offset_x + bx * scale, offset_y + by * scale
                self.draw_radial_cloud(gray_layer, px, py, max(bw, bh) * scale * 1.5, self.get_heat_intensity(count))

        self.generate_and_bind_heatmap(self.ms_canvas, gray_layer, 'ms_photo')

        for btn, info in MOUSE_LAYOUT.items():
            bx, by, shape, bw, bh = info
            px, py = offset_x + bx * scale, offset_y + by * scale
            pw, ph = bw * scale, bh * scale
            
            count = self.mouse_counts.get(btn, 0)

            if btn == 'MClick':
                click_map = self.mouse_mappings.get("MClick_click", "")
                scroll_map = self.mouse_mappings.get("MClick_scroll", "")
                
                text_color = "#38BDF8" if count > 0 else "#64748B"
                title_text = f"{btn}\n({count})"
                font_size = self.get_adaptive_font_size_multiline(5.3 * scale, title_text, pw, ph)
                
                self.ms_canvas.create_text(
                    px, py - 12 * scale if (click_map or scroll_map) else py,
                    text=title_text,
                    fill=text_color, font=('Microsoft YaHei', font_size, 'bold'), justify=tk.CENTER
                )
                
                y_offset = 2 * scale
                if click_map:
                    m_font_size = self.get_adaptive_font_size_multiline(3.5 * scale, "压:" + click_map, pw, ph)
                    self.ms_canvas.create_text(
                        px, py + y_offset,
                        text="压:" + click_map, fill="#00FFC2", font=('Microsoft YaHei', m_font_size, 'normal'), justify=tk.CENTER
                    )
                    y_offset += 10 * scale
                if scroll_map:
                    m_font_size = self.get_adaptive_font_size_multiline(3.5 * scale, "滑:" + scroll_map, pw, ph)
                    self.ms_canvas.create_text(
                        px, py + y_offset,
                        text="滑:" + scroll_map, fill="#00FFC2", font=('Microsoft YaHei', m_font_size, 'normal'), justify=tk.CENTER
                    )
            else:
                mapping = self.mouse_mappings.get(btn, "")
                text_color = "#38BDF8" if count > 0 else "#64748B"
                title_text = f"{btn}\n({count})"
                font_size = self.get_adaptive_font_size_multiline(5.3 * scale, title_text, pw, ph)
                
                self.ms_canvas.create_text(
                    px, py - 4 if mapping else py, 
                    text=title_text, 
                    fill=text_color, font=('Microsoft YaHei', font_size, 'bold'), justify=tk.CENTER
                )
                if mapping:
                    m_font_size = self.get_adaptive_font_size_multiline(4.0 * scale, mapping, pw, ph)
                    self.ms_canvas.create_text(
                        px, py + int(12*scale), 
                        text=mapping, fill="#00FFC2", font=('Microsoft YaHei', m_font_size, 'normal'), justify=tk.CENTER
                    )

    def draw_gamepad_canvas(self):
        self.gp_canvas.delete("all")
        w = self.gp_canvas.winfo_width()
        h = self.gp_canvas.winfo_height()
        if w < 20 or h < 20: return

        scale = min(w / 500, h / 350)
        offset_x = (w - 500 * scale) / 2
        offset_y = (h - 350 * scale) / 2
        self.gp_scale_info = {'scale': scale, 'offset_x': offset_x, 'offset_y': offset_y}

        scaled_poly = []
        for px, py in GAMEPAD_BODY_POLY:
            scaled_poly.append(offset_x + px * scale)
            scaled_poly.append(offset_y + py * scale)
        self.gp_canvas.create_polygon(scaled_poly, smooth=True, fill="#131926", outline="#2F3B52", width=3)

        for btn, info in GAMEPAD_LAYOUT.items():
            bx, by, shape, bw, bh = info
            px, py = offset_x + bx * scale, offset_y + by * scale
            pw, ph = bw * scale, bh * scale
            if shape == 'circle':
                self.gp_canvas.create_oval(px - pw/2, py - ph/2, px + pw/2, py + ph/2, fill="#1B2230", outline="#2F3B52", width=1)
            else:
                self.gp_canvas.create_rectangle(px - pw/2, py - ph/2, px + pw/2, py + ph/2, fill="#1B2230", outline="#2F3B52", width=1)

        gray_layer = Image.new("L", (w, h), 0)
        for btn, info in GAMEPAD_LAYOUT.items():
            bx, by, shape, bw, bh = info
            count = self.gamepad_counts.get(btn, 0)
            if count > 0:
                px, py = offset_x + bx * scale, offset_y + by * scale
                self.draw_radial_cloud(gray_layer, px, py, max(bw, bh) * scale * 1.5, self.get_heat_intensity(count))

        self.generate_and_bind_heatmap(self.gp_canvas, gray_layer, 'gp_photo')

        for btn, info in GAMEPAD_LAYOUT.items():
            bx, by, shape, bw, bh = info
            px, py = offset_x + bx * scale, offset_y + by * scale
            pw, ph = bw * scale, bh * scale
            
            count = self.gamepad_counts.get(btn, 0)

            if btn in ('LStick', 'RStick'):
                click_map = self.gamepad_mappings.get(f"{btn}_click", "")
                push_map = self.gamepad_mappings.get(f"{btn}_push", "")
                
                text_color = "#38BDF8" if count > 0 else "#64748B"
                title_text = f"{btn}\n({count})"
                font_size = self.get_adaptive_font_size_multiline(5.6 * scale, title_text, pw, ph)
                
                self.gp_canvas.create_text(
                    px, py - 12 * scale if (click_map or push_map) else py,
                    text=title_text,
                    fill=text_color, font=('Microsoft YaHei', font_size, 'bold'), justify=tk.CENTER
                )
                
                y_offset = 2 * scale
                if click_map:
                    m_font_size = self.get_adaptive_font_size_multiline(3.8 * scale, "压:" + click_map, pw, ph)
                    self.gp_canvas.create_text(
                        px, py + y_offset,
                        text="压:" + click_map, fill="#00FFC2", font=('Microsoft YaHei', m_font_size, 'normal'), justify=tk.CENTER
                    )
                    y_offset += 10 * scale
                if push_map:
                    m_font_size = self.get_adaptive_font_size_multiline(3.8 * scale, "推:" + push_map, pw, ph)
                    self.gp_canvas.create_text(
                        px, py + y_offset,
                        text="推:" + push_map, fill="#00FFC2", font=('Microsoft YaHei', m_font_size, 'normal'), justify=tk.CENTER
                    )
            else:
                mapping = self.gamepad_mappings.get(btn, "")
                text_color = "#38BDF8" if count > 0 else "#64748B"
                title_text = f"{btn}\n({count})"
                font_size = self.get_adaptive_font_size_multiline(5.6 * scale, title_text, pw, ph)
                
                self.gp_canvas.create_text(
                    px, py - 4 if mapping else py, 
                    text=title_text, 
                    fill=text_color, font=('Microsoft YaHei', font_size, 'bold'), justify=tk.CENTER
                )
                if mapping:
                    m_font_size = self.get_adaptive_font_size_multiline(4.2 * scale, mapping, pw, ph)
                    self.gp_canvas.create_text(
                        px, py + int(12*scale), 
                        text=mapping, fill="#00FFC2", font=('Microsoft YaHei', m_font_size, 'normal'), justify=tk.CENTER
                    )

    def record_input(self, key_name, device, duration=0.0):
        if not self.is_monitoring or not self.start_time: return
        
        now_t = time.time()
        local_time = datetime.now()
        elapsed = local_time - self.start_time
        elapsed_str = str(elapsed).split('.')[0]
        
        self.current_period_count += 1
        self.all_input_timestamps.append(now_t) 
        mapping_desc = ""
        
        log_key_name = key_name
        
        if device == '键盘' and key_name in self.keyboard_counts:
            self.keyboard_counts[key_name] += 1
            self.keyboard_durations[key_name] += duration
            mapping_desc = self.keyboard_mappings.get(key_name, "")
        elif device == '鼠标':
            base_key = key_name
            if key_name == 'MClick_click':
                base_key = 'MClick'
                mapping_desc = self.mouse_mappings.get("MClick_click", "")
                log_key_name = "MClick (按压)"
            elif key_name in ('ScrollUp', 'ScrollDown'):
                mapping_desc = self.mouse_mappings.get("MClick_scroll", "")
                log_key_name = f"{key_name} (滑动)"
            else:
                mapping_desc = self.mouse_mappings.get(key_name, "")
            
            if base_key in self.mouse_counts:
                self.mouse_counts[base_key] += 1
                self.mouse_durations[base_key] += duration
        elif device == '手柄':
            base_key = key_name
            if key_name.endswith('_click') or key_name.endswith('_push'):
                base_key = key_name.split('_')[0]
                mapping_desc = self.gamepad_mappings.get(key_name, "")
                if key_name.endswith('_click'):
                    log_key_name = f"{base_key} (按压)"
                else:
                    log_key_name = f"{base_key} (推动)"
            else:
                mapping_desc = self.gamepad_mappings.get(key_name, "")
            
            if base_key in self.gamepad_counts:
                self.gamepad_counts[base_key] += 1
                self.gamepad_durations[base_key] += duration
        
        self.logs.append({
            "监测时间": elapsed_str,
            "本地时间": local_time.strftime("%H:%M:%S"),
            "输入设备": device,
            "输入按键": log_key_name,
            "功能映射描述": mapping_desc,
            "按压时长": round(duration, 3)
        })

        time_str = local_time.strftime("%H:%M:%S")
        log_line = f"[{time_str}] {device}: {log_key_name} (时长:{duration:.3f}s)"
        if mapping_desc:
            log_line = f"[{time_str}] {device}: {log_key_name} - {mapping_desc} (时长:{duration:.3f}s)"
        self.log_queue.put(log_line)
        self.trigger_redraw()

    def check_peak_events(self, now_t):
        if not self.is_monitoring: return
        
        self.all_input_timestamps = [t for t in self.all_input_timestamps if now_t - t <= 60.0]
        current_apm = len(self.all_input_timestamps)
        
        if current_apm >= self.peak_threshold:
            if self.current_peak_segment is None:
                elapsed_sec = int(now_t - self.start_time_seconds)
                self.current_peak_segment = {
                    "start_rel_sec": elapsed_sec,
                    "start_rel": self.format_elapsed_time(elapsed_sec),
                    "start_loc": datetime.now().strftime("%H:%M:%S"),
                    "end_rel_sec": elapsed_sec,
                    "end_rel": self.format_elapsed_time(elapsed_sec),
                    "end_loc": datetime.now().strftime("%H:%M:%S"),
                    "apms": [current_apm],
                    "start_t": now_t
                }
            else:
                elapsed_sec = int(now_t - self.start_time_seconds)
                self.current_peak_segment["end_rel_sec"] = elapsed_sec
                self.current_peak_segment["end_rel"] = self.format_elapsed_time(elapsed_sec)
                self.current_peak_segment["end_loc"] = datetime.now().strftime("%H:%M:%S")
                self.current_peak_segment["apms"].append(current_apm)
        else:
            if self.current_peak_segment is not None:
                self.peak_periods.append(self.current_peak_segment)
                self.current_peak_segment = None
        
        if self.peak_window and self.peak_window.winfo_exists():
            self.peak_window.draw_chart()

    def format_elapsed_time(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}h{m}m{s}s"
        return f"{m}m{s}s"

    def open_peak_chart_window(self):
        if self.peak_window and self.peak_window.winfo_exists():
            self.peak_window.lift()
        else:
            self.peak_window = PeakChartWindow(self.root, self)

    def start_monitoring(self):
        self.start_time = datetime.now()
        self.start_time_seconds = time.time()
        self.last_peak_check_time = time.time()
        self.logs.clear()
        self.freq_history.clear()
        self.current_period_count = 0
        self.last_period_time = time.time()
        self.active_presses.clear()
        self.all_input_timestamps.clear()
        self.peak_periods.clear()
        self.current_peak_segment = None
        
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break
        
        self.trigger_redraw()
        
        if self.monitor_mode == "keyboard_mouse":
            self.kb_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
            self.kb_listener.daemon = True
            self.kb_listener.start()
            
            self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click_event, on_scroll=self.on_mouse_scroll_event)
            self.mouse_listener.daemon = True
            self.mouse_listener.start()
        else:
            self.stop_gp_event.clear()
            self.gp_thread = threading.Thread(target=self.gamepad_poll_loop, daemon=True)
            self.gp_thread.start()

    def stop_monitoring(self):
        now_t = time.time()
        if self.current_peak_segment is not None:
            self.current_peak_segment["end_rel_sec"] = int(now_t - self.start_time_seconds)
            self.current_peak_segment["end_rel"] = self.format_elapsed_time(self.current_peak_segment["end_rel_sec"])
            self.current_peak_segment["end_loc"] = datetime.now().strftime("%H:%M:%S")
            self.peak_periods.append(self.current_peak_segment)
            self.current_peak_segment = None
        
        self.total_elapsed_seconds = int(now_t - self.start_time_seconds)

        if self.kb_listener:
            try:
                self.kb_listener.stop()
            except Exception:
                pass
            self.kb_listener = None
        if self.mouse_listener:
            try:
                self.mouse_listener.stop()
            except Exception:
                pass
            self.mouse_listener = None
        if self.gp_thread:
            self.stop_gp_event.set()
            self.gp_thread.join(timeout=0.2)
            self.gp_thread = None

    def get_kb_key_name(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                k_name = key.char.upper()
            else:
                k_name = key.name
            
            kb_map = {
                'space': 'Space', 'enter': 'Enter', 'shift': 'LShift', 'shift_r': 'RShift',
                'ctrl_l': 'LCtrl', 'ctrl_r': 'RCtrl', 'alt_l': 'LAlt', 'alt_r': 'RAlt',
                'tab': 'Tab', 'backspace': 'Back', 'caps_lock': 'Caps', 'esc': 'Esc'
            }
            return kb_map.get(k_name, k_name)
        except Exception:
            return None

    def on_key_press(self, key):
        k_name = self.get_kb_key_name(key)
        if k_name and k_name in KEYBOARD_LAYOUT:
            self.event_queue.put(('kb_press', k_name, time.time()))

    def on_key_release(self, key):
        k_name = self.get_kb_key_name(key)
        if k_name and k_name in KEYBOARD_LAYOUT:
            self.event_queue.put(('kb_release', k_name, time.time()))

    def on_mouse_click_event(self, x, y, button, pressed):
        btn_name = None
        if button == mouse.Button.left: btn_name = "LClick"
        elif button == mouse.Button.right: btn_name = "RClick"
        elif button == mouse.Button.middle: btn_name = "MClick"
        elif button == mouse.Button.x1: btn_name = "Mouse4"
        elif button == mouse.Button.x2: btn_name = "Mouse5"
        
        if btn_name:
            if btn_name == "MClick":
                btn_name = "MClick_click"
            self.event_queue.put(('ms_click', btn_name, pressed, time.time()))

    def on_mouse_scroll_event(self, x, y, dx, dy):
        if dy > 0:
            self.event_queue.put(('ms_scroll', 'ScrollUp', time.time()))
        elif dy < 0:
            self.event_queue.put(('ms_scroll', 'ScrollDown', time.time()))

    def gamepad_poll_loop(self):
        try:
            pygame.init()
            pygame.joystick.init()
            
            joystick = None
            if pygame.joystick.get_count() > 0:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()

            joy_buttons = {
                0: 'A', 1: 'B', 2: 'X', 3: 'Y',
                4: 'LB', 5: 'RB', 6: 'Back', 7: 'Start',
                8: 'LStick_click', 9: 'RStick_click'
            }
            
            states_keys = list(GAMEPAD_LAYOUT.keys()) + ['LStick_click', 'LStick_push', 'RStick_click', 'RStick_push']
            last_btn_states = {btn: False for btn in states_keys}
            STICK_THRESHOLD = 0.5
            
            while not self.stop_gp_event.is_set():
                pygame.event.pump()
                if pygame.joystick.get_count() == 0:
                    time.sleep(0.1)
                    continue
                if joystick is None:
                    joystick = pygame.joystick.Joystick(0)
                    joystick.init()

                current_states = {btn: False for btn in states_keys}

                for idx, btn_name in joy_buttons.items():
                    if idx < joystick.get_numbuttons() and joystick.get_button(idx):
                        current_states[btn_name] = True

                if joystick.get_numaxes() >= 6:
                    lt_val = joystick.get_axis(4)
                    rt_val = joystick.get_axis(5)
                    if lt_val > -0.4: current_states['LT'] = True
                    if rt_val > -0.4: current_states['RT'] = True

                if joystick.get_numaxes() >= 4:
                    lx, ly = joystick.get_axis(0), joystick.get_axis(1)
                    rx, ry = joystick.get_axis(2), joystick.get_axis(3)
                    if math.sqrt(lx**2 + ly**2) > STICK_THRESHOLD: current_states['LStick_push'] = True
                    if math.sqrt(rx**2 + ry**2) > STICK_THRESHOLD: current_states['RStick_push'] = True

                if joystick.get_numhats() > 0:
                    hat = joystick.get_hat(0)
                    if hat[1] == 1: current_states['D-Pad-Up'] = True
                    if hat[1] == -1: current_states['D-Pad-Down'] = True
                    if hat[0] == -1: current_states['D-Pad-Left'] = True
                    if hat[0] == 1: current_states['D-Pad-Right'] = True

                for btn, pressed in current_states.items():
                    was_pressed = last_btn_states[btn]
                    if pressed and not was_pressed:
                        self.event_queue.put(('gp_press', btn, time.time()))
                    elif not pressed and was_pressed:
                        self.event_queue.put(('gp_release', btn, time.time()))
                    last_btn_states[btn] = pressed

                time.sleep(0.015)
        except Exception as e:
            self.log_queue.put(f"[手柄错误] 监听线程异常: {str(e)}")
        finally:
            try:
                pygame.joystick.quit()
                pygame.quit()
            except Exception:
                pass

    def process_event_queue(self):
        while not self.event_queue.empty():
            try:
                ev = self.event_queue.get_nowait()
                ev_type = ev[0]
                
                if ev_type == 'kb_press':
                    _, k_name, t = ev
                    if k_name not in self.active_presses:
                        self.active_presses[k_name] = t
                
                elif ev_type == 'kb_release':
                    _, k_name, t = ev
                    start_t = self.active_presses.pop(k_name, None)
                    if start_t is not None:
                        self.record_input(k_name, '键盘', t - start_t)
                
                elif ev_type == 'ms_click':
                    _, btn_name, pressed, t = ev
                    if pressed:
                        self.active_presses[btn_name] = t
                    else:
                        start_t = self.active_presses.pop(btn_name, None)
                        duration = t - start_t if start_t else 0.05
                        self.record_input(btn_name, '鼠标', duration)
                
                elif ev_type == 'ms_scroll':
                    _, scroll_dir, t = ev
                    self.record_input(scroll_dir, '鼠标', 0.05)
                
                elif ev_type == 'gp_press':
                    _, btn_name, t = ev
                    if btn_name not in self.active_presses:
                        self.active_presses[btn_name] = t
                
                elif ev_type == 'gp_release':
                    _, btn_name, t = ev
                    start_t = self.active_presses.pop(btn_name, None)
                    duration = t - start_t if start_t else 0.05
                    self.record_input(btn_name, '手柄', duration)
            
            except queue.Empty:
                break

    def update_loop(self):
        if not self.root.winfo_exists():
            return
        
        now = time.time()
        is_seconds_mode = "每秒" in self.freq_unit_var.get()
        interval = 1.0 if is_seconds_mode else 60.0
        
        self.process_event_queue()
        
        if self.is_monitoring and self.start_time:
            dur = datetime.now() - self.start_time
            self.lbl_timer.config(text=f"⏱ {str(dur).split('.')[0]}")
            
            if now - self.last_period_time >= interval:
                self.freq_history.append(self.current_period_count)
                self.current_period_count = 0
                self.last_period_time = now
                self.draw_frequency_chart()
            
            unit_name = "秒" if is_seconds_mode else "分"
            self.lbl_speed_val.config(text=f"实时速度: {self.current_period_count} 次/{unit_name}")

            if now - self.last_peak_check_time >= 1.0:
                self.check_peak_events(now)
                self.last_peak_check_time = now

        has_new_logs = False
        while not self.log_queue.empty():
            try:
                line = self.log_queue.get_nowait()
                self.txt_log.insert(tk.END, line + "\n")
                self.txt_log.see(tk.END)
                has_new_logs = True
            except queue.Empty:
                break
        
        if has_new_logs:
            total_clicks = len(self.logs)
            self.lbl_key_counts.config(text=f"捕获输入: {total_clicks} 次")
        
        if self.need_redraw:
            try:
                self.redraw_all()
            except Exception:
                pass
            self.need_redraw = False

        self.root.after(100, self.update_loop)

    def toggle_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.btn_monitor.config(text="■ 停止监测")
            self.lbl_status_led.config(text="● ACTIVE", fg="#00FFC2")
            for btn in (self.btn_export_img, self.btn_export_csv, self.btn_mode_km, self.btn_mode_gp, self.btn_clear, self.spin_saturation):
                btn.config(state=tk.DISABLED)
            self.btn_peak_chart.config(state=tk.NORMAL) 
            self.start_monitoring()
        else:
            self.is_monitoring = False
            self.btn_monitor.config(text="▶ 开始监测")
            self.lbl_status_led.config(text="● IDLE", fg="#64748B")
            for btn in (self.btn_export_img, self.btn_export_csv, self.btn_mode_km, self.btn_mode_gp, self.btn_clear, self.spin_saturation):
                btn.config(state=tk.NORMAL)
            self.btn_peak_chart.config(state=tk.DISABLED) 
            self.stop_monitoring()
            self.trigger_redraw()

    def export_heatmap(self):
        if self.monitor_mode == "keyboard_mouse":
            if not messagebox.askyesno("导出热力图", "当前页面是【键鼠监测模式】，是否导出【键鼠热力合图】？"):
                return
            
            filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
            if not filepath: return
            
            out_img = Image.new("RGBA", (3840, 2160), (11, 15, 25, 255))
            draw = ImageDraw.Draw(out_img)
            
            S = 1.745
            V_off = 295.0
            
            kb_unit_w = (1600.0 / 16.0) * S
            kb_unit_h = (600.0 / 7.0) * S
            kb_start_x = 50.0 * S
            kb_start_y = 150.0 * S + V_off
            
            for key, info in KEYBOARD_LAYOUT.items():
                row, col, kw = info
                kx = kb_start_x + col * kb_unit_w
                ky = kb_start_y + row * kb_unit_h
                draw.rectangle([kx, ky, kx + (kw * kb_unit_w - 6.0 * S), ky + (kb_unit_h - 6.0 * S)], fill=(27, 34, 48, 255), outline=(47, 59, 82, 255), width=int(2 * S))
            
            ms_scale = 2.4 * S
            ms_offset_x = 1600.0 * S + (600.0 * S - 220.0 * ms_scale) / 2.0
            ms_offset_y = V_off + (900.0 * S - 350.0 * ms_scale) / 2.0
            
            draw.ellipse([ms_offset_x + 20.0*ms_scale, ms_offset_y + 10.0*ms_scale, ms_offset_x + 200.0*ms_scale, ms_offset_y + 340.0*ms_scale], outline=(47, 59, 82, 255), width=int(6 * S))
            for btn, info in MOUSE_LAYOUT.items():
                bx, by, shape, bw, bh = info
                px, py = ms_offset_x + bx * ms_scale, ms_offset_y + by * ms_scale
                pw, ph = bw * ms_scale, bh * ms_scale
                if shape == 'circle':
                    draw.ellipse([px - pw/2.0, py - ph/2.0, px + pw/2.0, py + ph/2.0], fill=(27, 34, 48, 255), outline=(47, 59, 82, 255), width=int(2 * S))
                else:
                    draw.rectangle([px - pw/2.0, py - ph/2.0, px + pw/2.0, py + ph/2.0], fill=(27, 34, 48, 255), outline=(47, 59, 82, 255), width=int(2 * S))
            
            gray_layer = Image.new("L", (3840, 2160), 0)
            for key, info in KEYBOARD_LAYOUT.items():
                row, col, kw = info
                count = self.keyboard_counts.get(key, 0)
                if count > 0:
                    kx = kb_start_x + col * kb_unit_w
                    ky = kb_start_y + row * kb_unit_h
                    kw_px = kw * kb_unit_w - 6.0 * S
                    kh_px = kb_unit_h - 6.0 * S
                    self.draw_radial_cloud(gray_layer, kx + kw_px/2.0, ky + kh_px/2.0, max(kw_px, kh_px)*1.3, self.get_heat_intensity(count))
            
            for btn, info in MOUSE_LAYOUT.items():
                bx, by, shape, bw, bh = info
                count = self.mouse_counts.get(btn, 0)
                if count > 0:
                    px, py = ms_offset_x + bx * ms_scale, ms_offset_y + by * ms_scale
                    self.draw_radial_cloud(gray_layer, px, py, max(bw, bh)*ms_scale*1.5, self.get_heat_intensity(count))
            
            heat_color = self.apply_lut_color(gray_layer)
            out_img = Image.alpha_composite(out_img, heat_color)
            
            draw = ImageDraw.Draw(out_img)
            f_normal = get_font(int(15 * S), False)
            f_bold = get_font(int(16 * S), True)
            
            for key, info in KEYBOARD_LAYOUT.items():
                row, col, kw = info
                count = self.keyboard_counts.get(key, 0)
                mapping = self.keyboard_mappings.get(key, "")
                kx = kb_start_x + col * kb_unit_w
                ky = kb_start_y + row * kb_unit_h
                kw_px = kw * kb_unit_w - 6.0 * S
                kh_px = kb_unit_h - 6.0 * S
                draw.text((kx + kw_px/2.0, ky + kh_px/2.0 - 4.0 * S), f"{key}\n({count})", fill=(56, 189, 248, 255), font=f_bold, anchor="mm", align="center")
                if mapping: 
                    draw.text((kx + kw_px/2.0, ky + kh_px - 12.0 * S), mapping, fill=(0, 255, 194, 255), font=f_normal, anchor="mm", align="center")
            
            for btn, info in MOUSE_LAYOUT.items():
                bx, by, shape, bw, bh = info
                count = self.mouse_counts.get(btn, 0)
                px, py = ms_offset_x + bx * ms_scale, ms_offset_y + by * ms_scale
                
                if btn == 'MClick':
                    click_map = self.mouse_mappings.get("MClick_click", "")
                    scroll_map = self.mouse_mappings.get("MClick_scroll", "")
                    draw.text((px, py - 12.0 * ms_scale if (click_map or scroll_map) else py - 4.0 * S), f"{btn}\n({count})", fill=(56, 189, 248, 255), font=f_bold, anchor="mm", align="center")
                    
                    y_offset = 2.0 * ms_scale
                    if click_map:
                        draw.text((px, py + y_offset), "压:" + click_map, fill=(0, 255, 194, 255), font=f_normal, anchor="mm", align="center")
                        y_offset += 10.0 * ms_scale
                    if scroll_map:
                        draw.text((px, py + y_offset), "滑:" + scroll_map, fill=(0, 255, 194, 255), font=f_normal, anchor="mm", align="center")
                else:
                    mapping = self.mouse_mappings.get(btn, "")
                    draw.text((px, py - 4.0 * S), f"{btn}\n({count})", fill=(56, 189, 248, 255), font=f_bold, anchor="mm", align="center")
                    if mapping: 
                        draw.text((px, py + 18.0 * S), mapping, fill=(0, 255, 194, 255), font=f_normal, anchor="mm", align="center")

            out_img.save(filepath, "PNG")
            messagebox.showinfo("成功", f"键鼠合并热力图已成功保存至:\n{filepath}")

        else:
            if not messagebox.askyesno("导出热力图", "当前页面是【手柄监测模式】，是否导出【手柄热力图】？"):
                return
            
            filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
            if not filepath: return

            out_img = Image.new("RGBA", (3840, 2160), (11, 15, 25, 255))
            draw = ImageDraw.Draw(out_img)
            
            scale = 6.0
            offset_x = (3840.0 - 500.0 * scale) / 2.0
            offset_y = (2160.0 - 350.0 * scale) / 2.0
            
            mapped_poly = []
            for px, py in GAMEPAD_BODY_POLY:
                mapped_poly.append((offset_x + px * scale, offset_y + py * scale))
            draw.polygon(mapped_poly, fill=(19, 25, 38, 255), outline=(47, 59, 82, 255), width=int(4 * scale / 2.0))

            for btn, info in GAMEPAD_LAYOUT.items():
                bx, by, shape, bw, bh = info
                px, py = offset_x + bx * scale, offset_y + by * scale
                pw, ph = bw * scale, bh * scale
                if shape == 'circle':
                    draw.ellipse([px - pw/2.0, py - ph/2.0, px + pw/2.0, py + ph/2.0], fill=(27, 34, 48, 255), outline=(47, 59, 82, 255), width=int(2 * scale / 2.0))
                else:
                    draw.rectangle([px - pw/2.0, py - ph/2.0, px + pw/2.0, py + ph/2.0], fill=(27, 34, 48, 255), outline=(47, 59, 82, 255), width=int(2 * scale / 2.0))

            gray_layer = Image.new("L", (3840, 2160), 0)
            for btn, info in GAMEPAD_LAYOUT.items():
                bx, by, shape, bw, bh = info
                count = self.gamepad_counts.get(btn, 0)
                if count > 0:
                    px, py = offset_x + bx * scale, offset_y + by * scale
                    self.draw_radial_cloud(gray_layer, px, py, max(bw, bh)*scale*1.5, self.get_heat_intensity(count))

            heat_color = self.apply_lut_color(gray_layer)
            out_img = Image.alpha_composite(out_img, heat_color)
            
            draw = ImageDraw.Draw(out_img)
            f_normal = get_font(int(4.5 * scale), False)
            f_bold = get_font(int(5.0 * scale), True)
            
            for btn, info in GAMEPAD_LAYOUT.items():
                bx, by, shape, bw, bh = info
                count = self.gamepad_counts.get(btn, 0)
                px, py = offset_x + bx * scale, offset_y + by * scale
                
                if btn in ('LStick', 'RStick'):
                    click_map = self.gamepad_mappings.get(f"{btn}_click", "")
                    push_map = self.gamepad_mappings.get(f"{btn}_push", "")
                    draw.text((px, py - 12.0 * scale / 2.0 if (click_map or push_map) else py - 4.0 * scale / 2.0), f"{btn}\n({count})", fill=(56, 189, 248, 255), font=f_bold, anchor="mm", align="center")
                    
                    y_offset = 2.0 * scale / 2.0
                    if click_map:
                        draw.text((px, py + y_offset), "压:" + click_map, fill=(0, 255, 194, 255), font=f_normal, anchor="mm", align="center")
                        y_offset += 10.0 * scale / 2.0
                    if push_map:
                        draw.text((px, py + y_offset), "推:" + push_map, fill=(0, 255, 194, 255), font=f_normal, anchor="mm", align="center")
                else:
                    mapping = self.gamepad_mappings.get(btn, "")
                    draw.text((px, py - 4.0 * scale / 2.0), f"{btn}\n({count})", fill=(56, 189, 248, 255), font=f_bold, anchor="mm", align="center")
                    if mapping: 
                        draw.text((px, py + 15.0 * scale / 2.0), mapping, fill=(0, 255, 194, 255), font=f_normal, anchor="mm", align="center")

            out_img.save(filepath, "PNG")
            messagebox.showinfo("成功", f"手柄热力图已成功保存至:\n{filepath}")

    def export_log(self):
        try:
            import openpyxl
        except ImportError:
            messagebox.showerror("依赖缺失", "导出 Excel 数据表需要依赖库 'openpyxl'，请先在控制台执行以下命令进行安装：\npip install openpyxl")
            return

        if not self.logs:
            messagebox.showwarning("提示", "当前无任何监测日志数据。")
            return
        
        current_mode_cn = "键鼠监测模式" if self.monitor_mode == "keyboard_mouse" else "手柄监测模式"
        if not messagebox.askyesno("导出数据表", f"当前页面是【{current_mode_cn}】，是否导出对应控制器的统计数据表？"):
            return
        
        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel OpenXML Table", "*.xlsx")])
        if not filepath: return
        
        raw_df = pd.DataFrame(self.logs)
        
        stats_rows = []
        idx = 1
        if self.monitor_mode == "keyboard_mouse":
            df_records = raw_df[raw_df["输入设备"].isin(["键盘", "鼠标"])].copy()
            
            for k in KEYBOARD_LAYOUT.keys():
                count = self.keyboard_counts.get(k, 0)
                if count > 0:
                    stats_rows.append({
                        "序号": idx, "输入按键": k, "映射功能描述": self.keyboard_mappings.get(k, ""),
                        "按键次数": count, "总计按压时长(秒)": round(self.keyboard_durations.get(k, 0.0), 3)
                    })
                    idx += 1
            for m in MOUSE_LAYOUT.keys():
                count = self.mouse_counts.get(m, 0)
                if count > 0:
                    if m == 'MClick':
                        click_m = self.mouse_mappings.get("MClick_click", "")
                        scroll_m = self.mouse_mappings.get("MClick_scroll", "")
                        desc = f"按压: {click_m} | 滑动: {scroll_m}" if (click_m or scroll_m) else ""
                    else:
                        desc = self.mouse_mappings.get(m, "")
                    stats_rows.append({
                        "序号": idx, "输入按键": m, "映射功能描述": desc,
                        "按键次数": count, "总计按压时长(秒)": round(self.mouse_durations.get(m, 0.0), 3)
                    })
                    idx += 1
        else:
            df_records = raw_df[raw_df["输入设备"] == "手柄"].copy()
            
            for g in GAMEPAD_LAYOUT.keys():
                count = self.gamepad_counts.get(g, 0)
                if count > 0:
                    if g in ('LStick', 'RStick'):
                        click_g = self.gamepad_mappings.get(f"{g}_click", "")
                        push_g = self.gamepad_mappings.get(f"{g}_push", "")
                        desc = f"按压: {click_g} | 推动: {push_g}" if (click_g or push_g) else ""
                    else:
                        desc = self.gamepad_mappings.get(g, "")
                    stats_rows.append({
                        "序号": idx, "输入按键": g, "映射功能描述": desc,
                        "按键次数": count, "总计按压时长(秒)": round(self.gamepad_durations.get(g, 0.0), 3)
                    })
                    idx += 1

        df_stats = pd.DataFrame(stats_rows)
        
        if not df_records.empty:
            df_records = df_records[["监测时间", "本地时间", "输入设备", "输入按键", "功能映射描述", "按压时长"]]
            df_records.columns = ["监测时间", "本地时间", "输入设备", "输入按键", "映射功能描述", "按压时长(秒)"]
            df_records.insert(0, '序号', range(1, len(df_records) + 1))
        else:
            df_records = pd.DataFrame(columns=["序号", "监测时间", "本地时间", "输入设备", "输入按键", "映射功能描述", "按压时长(秒)"])

        try:
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df_stats.to_excel(writer, sheet_name='操作输入统计表', index=False)
                df_records.to_excel(writer, sheet_name='操作输入记录表', index=False)
            messagebox.showinfo("成功", f"高级结构化多分页报表已成功生成：\n{filepath}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败！文件可能已被其他程序占用：\n{str(e)}")

    def on_app_close(self):
        self.is_monitoring = False
        try:
            self.stop_monitoring()
        except Exception:
            pass
        if self.peak_window and self.peak_window.winfo_exists():
            try:
                self.peak_window.destroy()
            except Exception:
                pass
        try:
            self.root.destroy()
        except Exception:
            pass
        os._exit(0)


class PeakChartWindow(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("玩家输入尖峰波段统计图 (天工游麟)")
        self.geometry("1000x600")
        self.configure(bg="#0B0F19")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self._exporting = False
        
        self.setup_ui()
        self.draw_chart()
        
    def setup_ui(self):
        top_frame = tk.Frame(self, bg="#0F172A", height=50)
        top_frame.pack(fill=tk.X, side=tk.TOP, padx=0, pady=0)
        
        tk.Label(top_frame, text="⚡ 尖峰输入阈值 (次/分钟):", font=('Microsoft YaHei', 10, 'bold'), bg="#0F172A", fg="#94A3B8").pack(side=tk.LEFT, padx=15, pady=10)
        
        self.var_threshold = tk.IntVar(value=self.app.peak_threshold)
        self.spin_thresh = ttk.Spinbox(top_frame, from_=10, to=10000, increment=10, textvariable=self.var_threshold, width=8, font=('Consolas', 10, 'bold'), style='Dark.TSpinbox')
        self.spin_thresh.pack(side=tk.LEFT, padx=5, pady=10)
        
        btn_apply = ttk.Button(top_frame, text="💾 确认保存", command=self.apply_threshold, width=10, style='Flat.TButton')
        btn_apply.pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_export = ttk.Button(top_frame, text="🖼 导出尖峰图", command=self.export_chart, width=12, style='Flat.TButton')
        btn_export.pack(side=tk.RIGHT, padx=15, pady=10)
        
        self.canvas = tk.Canvas(self, bg="#0F172A", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        self.canvas.bind("<Configure>", lambda e: self.draw_chart())
        
    def apply_threshold(self):
        try:
            val = self.var_threshold.get()
            if val <= 0: raise ValueError
            self.app.peak_threshold = val
            messagebox.showinfo("成功", f"尖峰输入阈值已成功设置为: {val} 次/分钟", parent=self)
            self.draw_chart()
        except Exception:
            messagebox.showerror("错误", "阈值必须是大于 0 的正整数！", parent=self)

    def draw_chart(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100 or h < 100: return
        
        self.canvas.create_text(w/2, 30, text="📈 玩家输入尖峰波段时间轴统计图", fill="#00F0FF", font=('Microsoft YaHei', 14, 'bold'))
        self.canvas.create_text(w/2, 55, text=f"当前触发阈值: {self.app.peak_threshold} 次/分钟 | 橙红色块代表超过阈值的时间段", fill="#64748B", font=('Microsoft YaHei', 9))
        
        margin_left = 100
        margin_right = 60
        axis_y = h - 100
        axis_w = w - margin_left - margin_right
        
        self.canvas.create_line(margin_left, axis_y, w - margin_right, axis_y, fill="#475569", width=2)
        
        now_t = time.time()
        if self.app.is_monitoring:
            total_sec = max(int(now_t - self.app.start_time_seconds), 60)
        else:
            total_sec = max(self.app.total_elapsed_seconds, 60)
        
        if total_sec <= 300:
            tick_interval = 30 
        elif total_sec <= 1800:
            tick_interval = 120 
        else:
            tick_interval = 300 
        
        num_ticks = total_sec // tick_interval
        for i in range(num_ticks + 1):
            tick_sec = i * tick_interval
            if tick_sec > total_sec: break
            
            px = margin_left + (tick_sec / total_sec) * axis_w
            self.canvas.create_line(px, axis_y, px, axis_y + 8, fill="#475569", width=1.5)
            
            m, s = divmod(tick_sec, 60)
            rel_lbl = f"{m}m{s}s"
            
            tick_time = self.app.start_time + timedelta(seconds=tick_sec) if self.app.start_time else datetime.now()
            abs_lbl = tick_time.strftime("%H:%M:%S")
            
            self.canvas.create_text(px, axis_y + 22, text=rel_lbl, fill="#94A3B8", font=('Consolas', 8, 'bold'))
            self.canvas.create_text(px, axis_y + 36, text=abs_lbl, fill="#64748B", font=('Consolas', 7))

        all_segments = list(self.app.peak_periods)
        if self.app.current_peak_segment is not None:
            all_segments.append(self.app.current_peak_segment)
        
        block_y1 = axis_y - 180
        block_y2 = axis_y - 15
        
        if not all_segments:
            self.canvas.create_text(w/2, (block_y1 + block_y2)/2, text="☕ 当前监测尚未捕获到超过阈值的输入尖峰...", fill="#64748B", font=('Microsoft YaHei', 11))
            return
        
        for seg in all_segments:
            s_sec = seg["start_rel_sec"]
            e_sec = seg.get("end_rel_sec", int(now_t - self.app.start_time_seconds))
            
            x1 = margin_left + (s_sec / total_sec) * axis_w
            x2 = margin_left + (e_sec / total_sec) * axis_w
            if x2 - x1 < 4: x2 = x1 + 4 
            
            self.canvas.create_rectangle(x1, block_y1, x2, block_y2, fill="#EF4444", outline="#F87171", width=1)
            
            apms = seg.get("apms", [0])
            avg_apm = int(sum(apms) / len(apms)) if apms else 0
            max_apm = max(apms) if apms else 0
            
            mid_x = (x1 + x2) / 2
            lbl_text = f"尖峰段\n{seg['start_rel']} - {seg.get('end_rel', '进行中')}\n(平均:{avg_apm}/分, 峰值:{max_apm})"
            
            if (x2 - x1) > 160:
                self.canvas.create_text(mid_x, (block_y1 + block_y2)/2, text=lbl_text, fill="#FFFFFF", font=('Microsoft YaHei', 8, 'bold'), justify=tk.CENTER)
            else:
                self.canvas.create_text(mid_x, block_y1 - 30, text=f"{seg['start_rel']}-{seg.get('end_rel','...')}\nMax:{max_apm}", fill="#F87171", font=('Microsoft YaHei', 8), justify=tk.CENTER)
                self.canvas.create_line(mid_x, block_y1 - 8, mid_x, block_y1, fill="#F87171", width=1)

    def export_chart(self):
        if self._exporting:
            return
        self._exporting = True
        
        try:
            now_t = time.time()
            if self.app.is_monitoring:
                total_sec = max(int(now_t - self.app.start_time_seconds), 1)
            else:
                total_sec = max(self.app.total_elapsed_seconds, 1)
            
            start_sec = 0
            end_sec = total_sec
            
            filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
            if not filepath: 
                return
            
            img = Image.new("RGBA", (3840, 2160), (11, 15, 25, 255))
            draw = ImageDraw.Draw(img)
            
            S = 2.1333
            
            f_title = get_font(int(36 * S), True)
            f_sub = get_font(int(20 * S), False)
            f_labels = get_font(int(16 * S), True)
            f_mono = get_font(int(16 * S), False)
            
            draw.text((1920, 60 * S), "玩家输入尖峰波段时间轴统计图", fill=(0, 240, 255, 255), font=f_title, anchor="mm")
            
            range_info = f"触发阈值: {self.app.peak_threshold} 次/分钟 | 天工游麟工作室出品"
            draw.text((1920, 110 * S), range_info, fill=(100, 116, 139, 255), font=f_sub, anchor="mm")
            
            margin_left = 150 * S
            margin_right = 100 * S
            axis_y = 800 * S
            axis_w = 3840 - margin_left - margin_right
            
            draw.line([(margin_left, axis_y), (3840 - margin_right, axis_y)], fill=(71, 85, 105, 255), width=int(4 * S))
            
            export_total_sec = max(1, end_sec - start_sec)
            
            if export_total_sec <= 300:
                tick_interval = 30
            elif export_total_sec <= 1800:
                tick_interval = 120
            else:
                tick_interval = 300
            
            first_tick = ((start_sec + tick_interval - 1) // tick_interval) * tick_interval
            for tick_sec in range(first_tick, end_sec + 1, tick_interval):
                rel_sec = tick_sec - start_sec
                px = margin_left + (rel_sec / export_total_sec) * axis_w
                draw.line([(px, axis_y), (px, axis_y + 12 * S)], fill=(71, 85, 105, 255), width=int(2 * S))
                
                m, s = divmod(tick_sec, 60)
                rel_lbl = f"{m}m{s}s"
                
                tick_time = self.app.start_time + timedelta(seconds=tick_sec) if self.app.start_time else datetime.now()
                abs_lbl = tick_time.strftime("%H:%M:%S")
                
                draw.text((px, axis_y + 30 * S), rel_lbl, fill=(148, 163, 184, 255), font=f_mono, anchor="mm")
                draw.text((px, axis_y + 55 * S), abs_lbl, fill=(100, 116, 139, 255), font=f_mono, anchor="mm")
            
            all_segments = list(self.app.peak_periods)
            if self.app.current_peak_segment is not None:
                all_segments.append(self.app.current_peak_segment)
            
            block_y1 = axis_y - 250 * S
            block_y2 = axis_y - 20 * S
            
            rendered_segments = []
            for seg in all_segments:
                s_sec = seg["start_rel_sec"]
                e_sec = seg.get("end_rel_sec", int(now_t - self.app.start_time_seconds))
                
                draw_s_sec = max(s_sec, start_sec)
                draw_e_sec = min(e_sec, end_sec)
                
                if draw_s_sec < draw_e_sec:
                    rendered_segments.append((seg, draw_s_sec, draw_e_sec, e_sec))
            
            if not rendered_segments:
                draw.text((1920, 1080), "当前选定时间区间内暂无超出阈值的输入尖峰", fill=(100, 116, 139, 255), font=f_sub, anchor="mm")
            else:
                for seg, draw_s_sec, draw_e_sec, real_end_sec in rendered_segments:
                    x1 = margin_left + ((draw_s_sec - start_sec) / export_total_sec) * axis_w
                    x2 = margin_left + ((draw_e_sec - start_sec) / export_total_sec) * axis_w
                    if x2 - x1 < 6 * S: 
                        x2 = x1 + 6 * S
                    
                    draw.rectangle([x1, block_y1, x2, block_y2], fill=(239, 68, 68, 255), outline=(248, 113, 113, 255), width=int(2 * S))
                    
                    seg_start_t = seg["start_t"]
                    apms = seg.get("apms", [0])
                    filtered_apms = []
                    for i, apm_val in enumerate(apms):
                        point_t = seg_start_t + i
                        point_rel_sec = int(point_t - self.app.start_time_seconds)
                        if start_sec <= point_rel_sec <= end_sec:
                            filtered_apms.append(apm_val)
                    if not filtered_apms:
                        filtered_apms = [0]
                    
                    avg_apm = int(sum(filtered_apms) / len(filtered_apms))
                    max_apm = max(filtered_apms)
                    
                    mid_x = (x1 + x2) / 2
                    
                    m1, s1 = divmod(draw_s_sec, 60)
                    fmt_s = f"{m1}m{s1}s"
                    
                    if real_end_sec <= end_sec:
                        m2, s2 = divmod(draw_e_sec, 60)
                        fmt_e = f"{m2}m{s2}s"
                    else:
                        fmt_e = "进行中"
                    
                    lbl_text = f"尖峰段\n{fmt_s} - {fmt_e}\n(平均: {avg_apm}/分, 峰值: {max_apm})"
                    
                    if (x2 - x1) > 300 * S:
                        draw.text((mid_x, (block_y1 + block_y2)/2.0), lbl_text, fill=(255, 255, 255, 255), font=f_labels, anchor="mm", align="center")
                    else:
                        draw.text((mid_x, block_y1 - 60 * S), f"{fmt_s}-{fmt_e}\nMax APM: {max_apm}", fill=(248, 113, 113, 255), font=f_labels, anchor="mm", align="center")
                        draw.line([(mid_x, block_y1 - 20 * S), (mid_x, block_y1)], fill=(248, 113, 113, 255), width=int(2 * S))
            
            img.save(filepath, "PNG")
            messagebox.showinfo("成功", f"尖峰波段统计图已成功保存至:\n{filepath}", parent=self)
        finally:
            self._exporting = False

    def on_close(self):
        self.app.peak_window = None
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = InputTrackerApp(root)
    root.mainloop()