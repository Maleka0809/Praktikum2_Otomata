import tkinter as tk
import customtkinter as ctk

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PDASimulator:
    def __init__(self, input_string):
        self.input_string = input_string
        # Use list for tape. Empty input string is represented by empty list.
        self.tape = list(input_string) if input_string else []
        self.stack = []
        self.current_node = "READ_1"
        self.prev_node = "START"
        self.steps = []
        self.is_done = False
        self.result = None  # True: Accept, False: Reject
        
        # Initial step
        self.steps.append({
            "step_num": 0,
            "current_node": "START",
            "prev_node": "START",
            "tape": self.get_tape_string(),
            "stack": list(self.stack),
            "action": "Memulai simulasi PDA",
            "tape_read_index": 0
        })

    def get_tape_string(self):
        return "".join(self.tape) if self.tape else "λ"

    def step(self):
        if self.is_done:
            return self.result, self.steps

        step_num = len(self.steps)
        prev_node_val = self.steps[-1]["current_node"] if self.steps else "START"
        tape_read_idx = len(self.input_string) - len(self.tape)

        if self.current_node == "READ_1":
            if len(self.tape) > 0 and self.tape[0] == 'a':
                char = self.tape.pop(0)
                self.current_node = "PUSH_a"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "READ_1",
                    "prev_node": prev_node_val,
                    "tape": self.get_tape_string(),
                    "stack": list(self.stack),
                    "action": f"Membaca '{char}' -> transisi ke PUSH a",
                    "tape_read_index": tape_read_idx
                })
            elif len(self.tape) > 0 and self.tape[0] == 'b':
                char = self.tape.pop(0)
                self.current_node = "POP_1"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "READ_1",
                    "prev_node": prev_node_val,
                    "tape": self.get_tape_string(),
                    "stack": list(self.stack),
                    "action": f"Membaca '{char}' -> transisi ke POP 1",
                    "tape_read_index": tape_read_idx
                })
            elif len(self.tape) == 0:
                self.current_node = "POP_2"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "READ_1",
                    "prev_node": prev_node_val,
                    "tape": "λ",
                    "stack": list(self.stack),
                    "action": "Membaca λ (pita habis) -> transisi ke POP 2",
                    "tape_read_index": tape_read_idx
                })
            else:
                self.current_node = "REJECT"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "READ_1",
                    "prev_node": prev_node_val,
                    "tape": self.get_tape_string(),
                    "stack": list(self.stack),
                    "action": f"Membaca karakter tidak valid '{self.tape[0]}' -> transisi ke REJECT",
                    "tape_read_index": tape_read_idx
                })

        elif self.current_node == "PUSH_a":
            self.stack.append('a')
            self.current_node = "READ_1"
            self.steps.append({
                "step_num": step_num,
                "current_node": "PUSH_a",
                "prev_node": prev_node_val,
                "tape": self.get_tape_string(),
                "stack": list(self.stack),
                "action": "Push 'a' ke stack -> transisi kembali ke READ 1",
                "tape_read_index": max(0, tape_read_idx - 1)
            })

        elif self.current_node == "POP_1":
            if len(self.stack) > 0:
                popped = self.stack.pop()
                if popped == 'a':
                    self.current_node = "READ_2"
                    self.steps.append({
                        "step_num": step_num,
                        "current_node": "POP_1",
                        "prev_node": prev_node_val,
                        "tape": self.get_tape_string(),
                        "stack": list(self.stack),
                        "action": f"Pop dari stack, dapat '{popped}' -> transisi ke READ 2",
                        "tape_read_index": max(0, tape_read_idx - 1)
                    })
                else:
                    self.current_node = "REJECT"
                    self.steps.append({
                        "step_num": step_num,
                        "current_node": "POP_1",
                        "prev_node": prev_node_val,
                        "tape": self.get_tape_string(),
                        "stack": list(self.stack),
                        "action": f"Pop dari stack, dapat '{popped}' (bukan 'a') -> transisi ke REJECT",
                        "tape_read_index": max(0, tape_read_idx - 1)
                    })
            else:
                self.current_node = "REJECT"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "POP_1",
                    "prev_node": prev_node_val,
                    "tape": self.get_tape_string(),
                    "stack": list(self.stack),
                    "action": "Pop dari stack, stack kosong (λ) -> transisi ke REJECT",
                    "tape_read_index": max(0, tape_read_idx - 1)
                })

        elif self.current_node == "READ_2":
            if len(self.tape) > 0 and self.tape[0] == 'b':
                char = self.tape.pop(0)
                self.current_node = "POP_1"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "READ_2",
                    "prev_node": prev_node_val,
                    "tape": self.get_tape_string(),
                    "stack": list(self.stack),
                    "action": f"Membaca '{char}' -> transisi ke POP 1",
                    "tape_read_index": tape_read_idx
                })
            elif len(self.tape) > 0 and self.tape[0] == 'a':
                char = self.tape.pop(0)
                self.current_node = "REJECT"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "READ_2",
                    "prev_node": prev_node_val,
                    "tape": self.get_tape_string(),
                    "stack": list(self.stack),
                    "action": f"Membaca '{char}' (setelah 'b' tidak boleh ada 'a') -> transisi ke REJECT",
                    "tape_read_index": tape_read_idx
                })
            elif len(self.tape) == 0:
                self.current_node = "POP_2"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "READ_2",
                    "prev_node": prev_node_val,
                    "tape": "λ",
                    "stack": list(self.stack),
                    "action": "Membaca λ (pita habis) -> transisi ke POP 2",
                    "tape_read_index": tape_read_idx
                })
            else:
                self.current_node = "REJECT"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "READ_2",
                    "prev_node": prev_node_val,
                    "tape": self.get_tape_string(),
                    "stack": list(self.stack),
                    "action": f"Membaca karakter tidak valid '{self.tape[0]}' -> transisi ke REJECT",
                    "tape_read_index": tape_read_idx
                })

        elif self.current_node == "POP_2":
            if len(self.stack) == 0:
                self.current_node = "ACCEPT"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "POP_2",
                    "prev_node": prev_node_val,
                    "tape": "λ",
                    "stack": list(self.stack),
                    "action": "Pop dari stack, stack kosong (λ) -> transisi ke ACCEPT",
                    "tape_read_index": tape_read_idx
                })
            else:
                popped = self.stack.pop()
                self.current_node = "REJECT"
                self.steps.append({
                    "step_num": step_num,
                    "current_node": "POP_2",
                    "prev_node": prev_node_val,
                    "tape": "λ",
                    "stack": list(self.stack),
                    "action": f"Pop dari stack, dapat '{popped}' (masih tersisa sisa karakter) -> transisi ke REJECT",
                    "tape_read_index": tape_read_idx
                })

        elif self.current_node == "ACCEPT":
            self.is_done = True
            self.result = True
            self.steps.append({
                "step_num": step_num,
                "current_node": "ACCEPT",
                "prev_node": prev_node_val,
                "tape": "λ",
                "stack": list(self.stack),
                "action": "String DITERIMA (ACCEPTED)",
                "tape_read_index": tape_read_idx
            })

        elif self.current_node == "REJECT":
            self.is_done = True
            self.result = False
            self.steps.append({
                "step_num": step_num,
                "current_node": "REJECT",
                "prev_node": prev_node_val,
                "tape": self.get_tape_string(),
                "stack": list(self.stack),
                "action": "String DITOLAK (REJECTED)",
                "tape_read_index": tape_read_idx
            })

        return self.result, self.steps


class PDAGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Praktikum 2 - Simulator PDA (L = a^n b^n)")
        self.geometry("1200x750")
        self.resizable(True, True)

        # Simulator State
        self.sim = None
        self.step_idx = 0
        self.trace_history = []
        self.auto_play_job = None

        # Configure Grid Layout
        self.grid_columnconfigure(0, weight=2)  # Left panel (Controls & Input)
        self.grid_columnconfigure(1, weight=5)  # Middle panel (Visualizer)
        self.grid_columnconfigure(2, weight=3)  # Right panel (Logs & Trace)
        self.grid_rowconfigure(0, weight=1)

        # Create UI panels
        self.create_left_panel()
        self.create_middle_panel()
        self.create_right_panel()

        # Initial Draw
        self.canvas_flow.bind("<Configure>", self.on_canvas_resize)
        self.draw_stack_and_tape_inactive()

    def create_left_panel(self):
        left_frame = ctk.CTkFrame(self, corner_radius=10, width=280)
        left_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)

        # Title
        title_label = ctk.CTkLabel(
            left_frame, text="PDA SIMULATOR",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack(pady=(20, 5))

        subtitle_label = ctk.CTkLabel(
            left_frame, text="Bahasa L = { aⁿbⁿ | n ≥ 0 }",
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color="#90CAF9"
        )
        subtitle_label.pack(pady=(0, 20))

        # Input Section
        ctk.CTkLabel(
            left_frame, text="Masukkan String Tape:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 2))

        self.entry_string = ctk.CTkEntry(
            left_frame, placeholder_text="Contoh: aabb atau kosong (λ)",
            font=("Consolas", 14), height=35
        )
        self.entry_string.pack(fill="x", padx=20, pady=5)
        self.entry_string.insert(0, "aabb")

        # Preset Buttons
        preset_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        preset_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(preset_frame, text="Presets:").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))

        presets = ["λ", "ab", "aabb", "aaabbb", "aab", "abb", "aba"]
        for idx, preset in enumerate(presets):
            row = (idx // 3) + 1
            col = idx % 3
            btn = ctk.CTkButton(
                preset_frame, text="empty" if preset == "λ" else preset,
                width=65, height=25, fg_color="#37474F", hover_color="#455A64",
                command=lambda p=preset: self.load_preset(p)
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="ew")

        # Controls Section
        ctk.CTkLabel(
            left_frame, text="Kontrol Simulasi:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 2))

        self.btn_start = ctk.CTkButton(
            left_frame, text="Mulai Simulasi",
            fg_color="#1E88E5", hover_color="#1565C0", height=35,
            command=self.start_simulation
        )
        self.btn_start.pack(fill="x", padx=20, pady=5)

        self.btn_next = ctk.CTkButton(
            left_frame, text="Langkah Berikutnya (Next)",
            fg_color="#43A047", hover_color="#2E7D32", height=35,
            state="disabled", command=self.next_step
        )
        self.btn_next.pack(fill="x", padx=20, pady=5)

        self.btn_autoplay = ctk.CTkButton(
            left_frame, text="Auto Play",
            fg_color="#00ACC1", hover_color="#00838F", height=35,
            command=self.start_auto_play
        )
        self.btn_autoplay.pack(fill="x", padx=20, pady=5)

        self.btn_instant = ctk.CTkButton(
            left_frame, text="Simulasi Instan",
            fg_color="#FF8F00", hover_color="#FF6F00", height=35,
            command=self.instant_simulation
        )
        self.btn_instant.pack(fill="x", padx=20, pady=5)

        self.btn_reset = ctk.CTkButton(
            left_frame, text="Reset",
            fg_color="#D32F2F", hover_color="#C62828", height=35,
            command=self.reset_all
        )
        self.btn_reset.pack(fill="x", padx=20, pady=5)

        # Legend/Guide
        legend_frame = ctk.CTkFrame(left_frame, fg_color="#263238", corner_radius=8)
        legend_frame.pack(fill="x", padx=20, pady=(25, 20))
        
        legend_text = (
            "Keterangan Node:\n"
            "• READ: Membaca input tape\n"
            "• PUSH: Memasukkan 'a' ke stack\n"
            "• POP: Mengeluarkan 'a' dari stack\n"
            "• λ: Transisi string kosong\n"
            "• ACCEPT / REJECT: Hasil akhir"
        )
        ctk.CTkLabel(
            legend_frame, text=legend_text, justify="left",
            font=ctk.CTkFont(size=11), text_color="#CFD8DC"
        ).pack(padx=10, pady=10)

    def create_middle_panel(self):
        mid_frame = ctk.CTkFrame(self, fg_color="transparent")
        mid_frame.grid(row=0, column=1, padx=10, pady=15, sticky="nsew")
        mid_frame.grid_rowconfigure(0, weight=3) # Flowchart Canvas
        mid_frame.grid_rowconfigure(1, weight=2) # Tape & Stack Frame
        mid_frame.grid_columnconfigure(0, weight=1)

        # Flowchart Canvas
        flowchart_title = ctk.CTkLabel(
            mid_frame, text="Diagram Alir PDA (State Flowchart)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        flowchart_title.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 2))
        
        self.canvas_flow = tk.Canvas(
            mid_frame, bg="#121212", highlightthickness=1, highlightbackground="#2A2A2A"
        )
        self.canvas_flow.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Stack & Tape Container
        viz_container = ctk.CTkFrame(mid_frame, fg_color="transparent")
        viz_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        viz_container.grid_rowconfigure(0, weight=1)
        viz_container.grid_columnconfigure(0, weight=3) # Stack
        viz_container.grid_columnconfigure(1, weight=5) # Tape

        # Stack Frame
        stack_frame = ctk.CTkFrame(viz_container, corner_radius=8)
        stack_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        stack_frame.grid_rowconfigure(1, weight=1)
        stack_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            stack_frame, text="Pushdown Stack", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, pady=5)

        self.canvas_stack = tk.Canvas(
            stack_frame, bg="#1E1E1E", highlightthickness=0
        )
        self.canvas_stack.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Tape Frame
        tape_frame = ctk.CTkFrame(viz_container, corner_radius=8)
        tape_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        tape_frame.grid_rowconfigure(1, weight=1)
        tape_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            tape_frame, text="Pita Input (Input Tape)", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, pady=5)

        self.canvas_tape = tk.Canvas(
            tape_frame, bg="#1E1E1E", highlightthickness=0
        )
        self.canvas_tape.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def create_right_panel(self):
        right_frame = ctk.CTkFrame(self, corner_radius=10)
        right_frame.grid(row=0, column=2, padx=15, pady=15, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(4, weight=1)

        # Status Banner
        self.status_banner = ctk.CTkLabel(
            right_frame, text="SIAP DIJALANKAN",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#37474F", text_color="#FFFFFF",
            corner_radius=8, height=45
        )
        self.status_banner.grid(row=0, column=0, padx=15, pady=15, sticky="ew")

        # Tape Remaining Display
        ctk.CTkLabel(
            right_frame, text="Pita Input Saat Ini:", font=ctk.CTkFont(weight="bold")
        ).grid(row=1, column=0, padx=15, sticky="w")
        
        self.lbl_tape_rem = ctk.CTkLabel(
            right_frame, text="-", font=("Consolas", 18, "bold"), text_color="#FFD54F"
        )
        self.lbl_tape_rem.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="w")

        # Step Logs Textbox
        ctk.CTkLabel(
            right_frame, text="Log Transisi Langkah:", font=ctk.CTkFont(weight="bold")
        ).grid(row=3, column=0, padx=15, sticky="w")

        self.txt_logs = ctk.CTkTextbox(
            right_frame, font=("Consolas", 12), fg_color="#121212"
        )
        self.txt_logs.grid(row=4, column=0, padx=15, pady=(5, 15), sticky="nsew")

    def load_preset(self, text):
        self.reset_all()
        self.entry_string.delete(0, tk.END)
        if text != "λ":
            self.entry_string.insert(0, text)

    def draw_flowchart_inactive(self):
        self.canvas_flow.delete("all")
        
        # Get canvas size
        w = self.canvas_flow.winfo_width()
        h = self.canvas_flow.winfo_height()
        # Fallback if canvas is not drawn yet
        if w <= 1: w = 580
        if h <= 1: h = 320

        # Flowchart drawing bounds:
        # width = 510 (from x=70 to x=580)
        # height = 310 (from y=10 to y=320)
        dx = (w - 510) / 2 - 70
        dy = (h - 310) / 2 - 10

        # Coordinates and properties of nodes
        self.nodes = {
            "START": {"type": "rect", "coords": (210 + dx, 10 + dy, 290 + dx, 40 + dy), "label": "START"},
            "READ_1": {"type": "diamond", "coords": (250 + dx, 105 + dy, 50, 30), "label": "READ 1"}, # Center X, Center Y, half-w, half-h
            "PUSH_a": {"type": "rect", "coords": (70 + dx, 85 + dy, 150 + dx, 125 + dy), "label": "PUSH a"},
            "POP_1": {"type": "diamond", "coords": (250 + dx, 205 + dy, 50, 30), "label": "POP 1"},
            "READ_2": {"type": "diamond", "coords": (390 + dx, 205 + dy, 50, 30), "label": "READ 2"},
            "POP_2": {"type": "diamond", "coords": (510 + dx, 105 + dy, 50, 30), "label": "POP 2"},
            "ACCEPT": {"type": "rect", "coords": (470 + dx, 185 + dy, 550 + dx, 225 + dy), "label": "ACCEPT"},
            "REJECT": {"type": "rect", "coords": (350 + dx, 280 + dy, 430 + dx, 320 + dy), "label": "REJECT"},
        }

        # Draw transitions/lines first so they stay behind nodes
        self.transitions = {
            "START_READ_1": {"type": "line", "points": (250, 40, 250, 75), "label": ""},
            "READ_1_PUSH_a": {"type": "line", "points": (200, 105, 150, 105), "label": "a", "side": "top"},
            "PUSH_a_READ_1": {"type": "loop", "points": (110, 85, 110, 57, 250, 57), "label": ""},
            "READ_1_POP_1": {"type": "line", "points": (250, 135, 250, 175), "label": "b", "side": "right"},
            "POP_1_READ_2": {"type": "line", "points": (300, 205, 340, 205), "label": "a", "side": "top"},
            "READ_2_POP_1": {"type": "loop", "points": (390, 175, 390, 155, 250, 155), "label": "b", "label_coord": (320, 145)},
            "READ_2_POP_2": {"type": "loop", "points": (440, 205, 450, 205, 450, 120, 485, 120), "label": "λ", "label_coord": (462, 160)},
            "READ_1_POP_2": {"type": "line", "points": (300, 105, 460, 105), "label": "λ", "side": "top"},
            "POP_2_ACCEPT": {"type": "line", "points": (510, 135, 510, 185), "label": "λ", "side": "right"},
            "POP_1_REJECT": {"type": "loop2", "points": (250, 235, 250, 300, 350, 300), "label": "b, λ", "label_coord": (290, 310)},
            "READ_2_REJECT": {"type": "line", "points": (390, 235, 390, 280), "label": "a", "side": "right"},
            "POP_2_REJECT": {"type": "loop2", "points": (560, 105, 580, 105, 580, 300, 430, 300), "label": "a, b", "label_coord": (480, 310)},
        }

        # Apply offsets to transition points and label coordinates
        for name, data in self.transitions.items():
            pts = list(data["points"])
            for i in range(0, len(pts), 2):
                pts[i] += dx
                pts[i+1] += dy
            data["points"] = tuple(pts)
            
            if "label_coord" in data:
                lx, ly = data["label_coord"]
                data["label_coord"] = (lx + dx, ly + dy)

        # Draw transitions lines
        for name, data in self.transitions.items():
            pts = data["points"]
            if data["type"] == "line":
                self.canvas_flow.create_line(
                    *pts, arrow=tk.LAST, fill="#424242", width=2, tags=f"arrow_{name}"
                )
            else: # loop / custom paths
                self.canvas_flow.create_line(
                    *pts, arrow=tk.LAST, fill="#424242", width=2, tags=f"arrow_{name}"
                )
            
            # Draw labels for lines
            lbl = data["label"]
            if lbl:
                # Calculate middle point of first two points to place text
                if "label_coord" in data:
                    lx, ly = data["label_coord"]
                elif data["side"] == "top":
                    lx, ly = (pts[0] + pts[2]) / 2, (pts[1] + pts[3]) / 2 - 10
                elif data["side"] == "right":
                    lx, ly = (pts[0] + pts[2]) / 2 + 10, (pts[1] + pts[3]) / 2
                elif data["side"] == "bottom":
                    lx, ly = 290 + dx, 310 + dy
                elif data["side"] == "bottom_right":
                    lx, ly = 480 + dx, 310 + dy
                elif data["side"] == "top_right":
                    lx, ly = 320 + dx, 145 + dy
                else: # default
                    lx, ly = (pts[0] + pts[2]) / 2 + 10, (pts[1] + pts[3]) / 2 - 10
                self.canvas_flow.create_text(
                    lx, ly, text=lbl, fill="#9E9E9E", font=("Consolas", 10, "bold"), tags=f"label_{name}"
                )

        # Draw nodes
        for name, data in self.nodes.items():
            t = data["type"]
            c = data["coords"]
            lbl = data["label"]
            
            if t == "rect":
                self.canvas_flow.create_rectangle(
                    *c, fill="#212121", outline="#424242", width=2, tags=f"node_{name}"
                )
                self.canvas_flow.create_text(
                    (c[0] + c[2]) / 2, (c[1] + c[3]) / 2,
                    text=lbl, fill="#E0E0E0", font=("Helvetica", 11, "bold"), tags=f"text_{name}"
                )
            elif t == "diamond":
                # c is (cx, cy, hw, hh)
                cx, cy, hw, hh = c
                pts = (cx, cy - hh, cx + hw, cy, cx, cy + hh, cx - hw, cy)
                self.canvas_flow.create_polygon(
                    *pts, fill="#212121", outline="#424242", width=2, tags=f"node_{name}"
                )
                self.canvas_flow.create_text(
                    cx, cy, text=lbl, fill="#E0E0E0", font=("Helvetica", 11, "bold"), tags=f"text_{name}"
                )

    def highlight_node_and_edge(self, current_node, prev_node):
        # Reset all nodes to inactive
        for name, data in self.nodes.items():
            t = data["type"]
            self.canvas_flow.itemconfig(f"node_{name}", fill="#212121", outline="#424242")
            self.canvas_flow.itemconfig(f"text_{name}", fill="#E0E0E0")

        # Reset all transitions to inactive
        for name in self.transitions:
            self.canvas_flow.itemconfig(f"arrow_{name}", fill="#424242", width=2)
            self.canvas_flow.itemconfig(f"label_{name}", fill="#9E9E9E")

        # Highlight active node
        if current_node in self.nodes:
            color = "#1565C0"  # active blue
            if current_node == "ACCEPT":
                color = "#2E7D32"  # success green
            elif current_node == "REJECT":
                color = "#C62828"  # error red
            
            self.canvas_flow.itemconfig(f"node_{current_node}", fill=color, outline="#64B5F6")
            self.canvas_flow.itemconfig(f"text_{current_node}", fill="#FFFFFF")

        # Find edge to highlight based on transition
        transition_key = f"{prev_node}_{current_node}"
        if transition_key in self.transitions:
            self.canvas_flow.itemconfig(f"arrow_{transition_key}", fill="#FF9800", width=3)
            self.canvas_flow.itemconfig(f"label_{transition_key}", fill="#FFB74D")
        elif prev_node == "READ_1" and current_node == "READ_1": # PUSH loop back line sequence
            # PUSH loop triggers sequence READ_1 -> PUSH_a -> READ_1
            # We highlight READ_1_PUSH_a first, then PUSH_a_READ_1
            pass

    def draw_stack_and_tape_inactive(self):
        # Stack Canvas Drawing
        self.canvas_stack.delete("all")
        sw, sh = 180, 180
        # Draw test-tube/stack box
        self.canvas_stack.create_line(60, 20, 60, 150, fill="#757575", width=3) # left wall
        self.canvas_stack.create_line(120, 20, 120, 150, fill="#757575", width=3) # right wall
        self.canvas_stack.create_line(58, 150, 122, 150, fill="#757575", width=3) # bottom wall
        self.canvas_stack.create_text(90, 165, text="(Stack Kosong)", fill="#757575", font=("Consolas", 10))

        # Tape Canvas Drawing
        self.canvas_tape.delete("all")
        self.canvas_tape.create_text(250, 30, text="(Pita Kosong)", fill="#757575", font=("Consolas", 12))

    def on_canvas_resize(self, event):
        # Redraw flowchart based on the current step highlight
        if self.sim and self.trace_history and self.step_idx < len(self.trace_history):
            self.update_visuals(self.trace_history[self.step_idx])
        else:
            self.draw_flowchart_inactive()

    def update_visuals(self, step_data):
        # Redraw flowchart first to ensure it's centered and updated based on current canvas size
        self.draw_flowchart_inactive()

        # 1. Flowchart highlight
        current_node = step_data["current_node"]
        prev_node = step_data["prev_node"]
        
        # Determine previous node context
        if step_data["step_num"] > 0:
            p_node = self.trace_history[step_data["step_num"] - 1]["current_node"]
        else:
            p_node = "START"
        self.highlight_node_and_edge(current_node, p_node)

        # 2. Update Stack representation
        self.canvas_stack.delete("all")
        stack_list = step_data["stack"]
        
        # Redraw container
        self.canvas_stack.create_line(60, 20, 60, 150, fill="#757575", width=3)
        self.canvas_stack.create_line(120, 20, 120, 150, fill="#757575", width=3)
        self.canvas_stack.create_line(58, 150, 122, 150, fill="#757575", width=3)
        
        # Draw stack items
        # Height available: 130px. Each block ~20px high. Max ~6 items.
        y_bottom = 150
        block_h = 20
        for idx, item in enumerate(stack_list):
            if idx >= 6:
                # stack overflow display limit
                self.canvas_stack.create_text(90, 15, text="...", fill="#FF8F00", font=("Consolas", 12, "bold"))
                break
            y1 = y_bottom - (idx + 1) * block_h
            y2 = y_bottom - idx * block_h
            self.canvas_stack.create_rectangle(63, y1 + 1, 117, y2 - 1, fill="#1E88E5", outline="#90CAF9", width=1)
            self.canvas_stack.create_text(90, (y1 + y2) / 2, text=item, fill="#FFFFFF", font=("Consolas", 11, "bold"))
            
        stack_lbl_text = f"Stack size: {len(stack_list)}" if stack_list else "(Stack Kosong)"
        self.canvas_stack.create_text(90, 165, text=stack_lbl_text, fill="#E0E0E0", font=("Consolas", 10))

        # 3. Update Tape representation
        self.canvas_tape.delete("all")
        
        full_string = self.entry_string.get().strip()
        tape_chars = list(full_string) if full_string else ['λ']
        read_index = step_data["tape_read_index"]

        box_w = 32
        box_h = 32
        gap = 4
        total_len = len(tape_chars)
        total_w = total_len * box_w + (total_len - 1) * gap
        
        # Let's anchor Tape drawing inside canvas width 500
        start_x = max(20, (500 - total_w) / 2)
        y1, y2 = 15, 47

        for i, char in enumerate(tape_chars):
            x1 = start_x + i * (box_w + gap)
            x2 = x1 + box_w
            
            if i < read_index:
                # Read characters: greyed out
                bg_color = "#37474F"
                border_color = "#455A64"
                text_color = "#78909C"
                thickness = 1
            elif i == read_index and not self.sim.is_done:
                # Current reading character: golden border & active text
                bg_color = "#FF8F00"
                border_color = "#FFD54F"
                text_color = "#FFFFFF"
                thickness = 3
            else:
                # Future characters
                bg_color = "#212121"
                border_color = "#616161"
                text_color = "#E0E0E0"
                thickness = 1

            self.canvas_tape.create_rectangle(
                x1, y1, x2, y2, fill=bg_color, outline=border_color, width=thickness
            )
            self.canvas_tape.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2,
                text=char, fill=text_color, font=("Consolas", 14, "bold")
            )

        # Tape pointer indicator
        if read_index < len(tape_chars) and not self.sim.is_done:
            px = start_x + read_index * (box_w + gap) + box_w / 2
            self.canvas_tape.create_polygon(
                px, y2 + 5, px - 6, y2 + 13, px + 6, y2 + 13,
                fill="#FFD54F"
            )

    def log_step(self, step_data):
        step_num = step_data["step_num"]
        node = step_data["current_node"]
        tape_rem = step_data["tape"]
        stack_state = step_data["stack"]
        action = step_data["action"]

        stack_str = f"[{', '.join(stack_state)}]" if stack_state else "[]"
        
        log_entry = (
            f"[Langkah {step_num}]\n"
            f"  State Node : {node}\n"
            f"  Sisa Tape  : \"{tape_rem}\"\n"
            f"  Isi Stack  : {stack_str}\n"
            f"  Keterangan : {action}\n"
            f"{'-'*40}\n"
        )
        self.txt_logs.insert(tk.END, log_entry)
        self.txt_logs.see(tk.END)
        
        # Update current tape remaining label
        self.lbl_tape_rem.configure(text=f"\"{tape_rem}\"")

    def start_simulation(self):
        input_str = self.entry_string.get().strip()
        
        # Reset and Initialize Simulator
        self.txt_logs.delete("1.0", tk.END)
        self.sim = PDASimulator(input_str)
        self.trace_history = [self.sim.steps[0]]
        self.step_idx = 0

        # Cancel any running autoplay
        if hasattr(self, 'auto_play_job') and self.auto_play_job:
            self.after_cancel(self.auto_play_job)
            self.auto_play_job = None

        self.status_banner.configure(
            text="SIMULASI BERJALAN", fg_color="#FF8F00", text_color="#FFFFFF"
        )

        # Log & Draw first step
        self.log_step(self.trace_history[0])
        self.update_visuals(self.trace_history[0])

        # Enable/Disable Buttons
        self.btn_next.configure(state="normal")
        self.btn_autoplay.configure(state="normal")
        self.btn_start.configure(state="disabled")
        self.btn_instant.configure(state="disabled")
        self.entry_string.configure(state="disabled")

    def next_step(self):
        if not self.sim or self.sim.is_done:
            return

        res, steps = self.sim.step()
        self.trace_history = steps
        self.step_idx += 1
        
        current_step = self.trace_history[self.step_idx]
        self.log_step(current_step)
        self.update_visuals(current_step)

        if self.sim.is_done:
            self.finish_simulation(res)

    def instant_simulation(self):
        self.start_simulation()
        while self.sim and not self.sim.is_done:
            self.next_step()

    def start_auto_play(self):
        if not self.sim:
            self.start_simulation()
        self.btn_autoplay.configure(state="disabled")
        self.btn_next.configure(state="disabled")
        self.btn_instant.configure(state="disabled")
        self.auto_play_next()

    def auto_play_next(self):
        if self.sim and not self.sim.is_done:
            self.next_step()
            self.auto_play_job = self.after(750, self.auto_play_next)
        else:
            self.auto_play_job = None

    def finish_simulation(self, accepted):
        self.btn_next.configure(state="disabled")
        self.btn_autoplay.configure(state="disabled")
        
        if accepted:
            self.status_banner.configure(
                text="ACCEPTED (DITERIMA)", fg_color="#2E7D32", text_color="#FFFFFF"
            )
            self.txt_logs.insert(tk.END, ">>> KEPUTUSAN: STRING DITERIMA (ACCEPTED) <<<\n")
        else:
            self.status_banner.configure(
                text="REJECTED (DITOLAK)", fg_color="#C62828", text_color="#FFFFFF"
            )
            self.txt_logs.insert(tk.END, ">>> KEPUTUSAN: STRING DITOLAK (REJECTED) <<<\n")
            
        self.txt_logs.see(tk.END)

    def reset_all(self):
        # Cancel any running autoplay
        if hasattr(self, 'auto_play_job') and self.auto_play_job:
            self.after_cancel(self.auto_play_job)
            self.auto_play_job = None

        self.sim = None
        self.step_idx = 0
        self.trace_history = []
        
        self.txt_logs.delete("1.0", tk.END)
        self.lbl_tape_rem.configure(text="-")
        self.status_banner.configure(
            text="SIAP DIJALANKAN", fg_color="#37474F", text_color="#FFFFFF"
        )

        self.btn_start.configure(state="normal")
        self.btn_next.configure(state="disabled")
        self.btn_autoplay.configure(state="normal")
        self.btn_instant.configure(state="normal")
        self.entry_string.configure(state="normal")

        self.draw_flowchart_inactive()
        self.draw_stack_and_tape_inactive()


if __name__ == "__main__":
    app = PDAGUI()
    app.mainloop()
