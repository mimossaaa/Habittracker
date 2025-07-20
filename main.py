
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("1600x700")
        self.root.configure(bg="#f0f0f0")

        self.habits = ["Calculus", "Chemistry", "Reading", "Projects", "Exercise"]
        self.habit_states = [False] * len(self.habits)

        self.create_widgets()
        self.load_daily_habits_state()
        self.update_background()

    def create_widgets(self):
        left_frame = ttk.Frame(self.root, style="Main.TFrame")
        left_frame.pack(side="left", expand=True, fill="both", padx=(40, 20), pady=40)

        content_frame = ttk.Frame(left_frame, style="Main.TFrame")
        content_frame.pack(expand=True)

        self.root.style = ttk.Style()
        self.root.style.configure("Main.TFrame", background="#f0f0f0")
        self.root.style.configure("TButton", padding=10, font=("Helvetica", 12))
        self.root.style.configure("Header.TLabel", background="#f0f0f0", font=("Helvetica", 18, "bold"))
        self.root.style.configure("Puzzle.TLabel", background="#f0f0f0", font=("Helvetica", 14, "bold"))

        header_label = ttk.Label(content_frame, text="Track Your Habits", style="Header.TLabel")
        header_label.pack(pady=(0, 20))

        self.canvas = tk.Canvas(content_frame, width=300, height=300, bg="#f0f0f0", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.draw_pentagon()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        log_button = ttk.Button(content_frame, text="Log Habits", command=self.log_habits)
        log_button.pack(pady=20)

        right_frame = ttk.Frame(self.root, style="Main.TFrame")
        right_frame.pack(side="right", expand=True, fill="both", padx=(20, 40), pady=40)

        self.graph_frame = ttk.Frame(right_frame, style="Main.TFrame")
        self.graph_frame.pack(side="top", expand=True, fill="both", pady=(0, 20))
        
        self.puzzle_frame = ttk.Frame(right_frame, style="Main.TFrame")
        self.puzzle_frame.pack(side="bottom", expand=True, fill="both")

        self.puzzle_label = ttk.Label(self.puzzle_frame, text="Weekly Progress Puzzle", style="Puzzle.TLabel")
        self.puzzle_label.pack(pady=(10,10))

        height=220,   # <-- was 270; now matches 4 rows
        self.puzzle_canvas.pack(pady=10)

        self.update_graph()
        self.update_puzzle()

    def draw_pentagon(self):
        self.canvas.delete("all")
        center_x, center_y = 150, 150
        radius = 100
        self.triangle_ids = []
        for i in range(5):
            angle = (math.pi / 2.5) * i - math.pi / 2
            x1 = center_x + radius * math.cos(angle)
            y1 = center_y + radius * math.sin(angle)
            
            angle2 = (math.pi / 2.5) * (i + 1) - math.pi / 2
            x2 = center_x + radius * math.cos(angle2)
            y2 = center_y + radius * math.sin(angle2)
            
            color = "#4caf50" if self.habit_states[i] else "#cccccc"
            triangle = self.canvas.create_polygon(center_x, center_y, x1, y1, x2, y2, fill=color, outline="white", width=2)
            self.triangle_ids.append(triangle)

            label_angle = (angle + angle2) / 2
            label_x = center_x + (radius + 30) * math.cos(label_angle)
            label_y = center_y + (radius + 30) * math.sin(label_angle)
            self.canvas.create_text(label_x, label_y, text=self.habits[i], font=("Helvetica", 10, "bold"))

    def on_canvas_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        if item in self.triangle_ids:
            index = self.triangle_ids.index(item)
            self.habit_states[index] = not self.habit_states[index]
            self.draw_pentagon()
            self.update_background()

    def update_background(self, event=None):
        completed_habits = sum(self.habit_states)
        green_intensity = int(240 - (completed_habits / len(self.habits)) * 100)
        color = f"#{green_intensity:02x}{green_intensity:02x}{green_intensity:02x}"
        
        self.root.configure(bg=color)
        self.canvas.configure(bg=color)
        if hasattr(self, 'puzzle_canvas'):
            self.puzzle_canvas.configure(bg=color)
        self.root.style.configure("Main.TFrame", background=color)
        self.root.style.configure("Header.TLabel", background=color)
        self.root.style.configure("Puzzle.TLabel", background=color)

    def log_habits(self):
        data = self.load_data()
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        completed_today = [self.habits[i] for i, state in enumerate(self.habit_states) if state]
        
        data[today_str] = completed_today
        self.save_data(data)
        
        self.habit_states = [False] * len(self.habits)
        self.draw_pentagon()
        self.update_graph()
        self.update_puzzle()
        self.update_background()

    def load_daily_habits_state(self):
        data = self.load_data()
        today_str = datetime.now().strftime("%Y-%m-%d")
        if today_str in data:
            completed_today = data[today_str]
            for i, habit in enumerate(self.habits):
                if habit in completed_today:
                    self.habit_states[i] = True
        self.draw_pentagon()
        self.update_background()

    def load_data(self):
        try:
            with open("habits.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        with open("habits.json", "w") as f:
            json.dump(data, f, indent=4)

    def update_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        data = self.load_data()
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        week_dates = [(start_of_week + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        
        habits_completed = [len(data.get(date, [])) for date in week_dates]

        if not any(habits_completed):
            no_data_label = ttk.Label(self.graph_frame, text="No habit data for this week.", style="Header.TLabel")
            no_data_label.pack(expand=True)
            return

        fig, ax = plt.subplots(figsize=(5, 3), facecolor="#f0f0f0")
        ax.plot(week_dates, habits_completed, marker='o', linestyle='-', color='#4caf50', markerfacecolor='#4caf50', markersize=8)
        ax.set_xlabel("Date", color="#333333")
        ax.set_ylabel("Habits Completed", color="#333333")
        ax.set_title("Weekly Habit Progress", color="#333333")
        ax.set_yticks(range(6))
        ax.set_ylim(0, 5)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.set_facecolor("#ffffff")
        plt.xticks(rotation=45, ha="right", color="#333333")
        plt.yticks(color="#333333")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        plt.close(fig)

    def _create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """Draws a rounded rectangle on a canvas."""
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def update_puzzle(self):
        self.puzzle_canvas.delete("all")

        data = self.load_data()
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        week_dates = [(start_of_week + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        
        total_habits_this_week = sum(len(data.get(date, [])) for date in week_dates)

        canvas_width = 380
        canvas_height = 270
        
        rows, cols = 4, 7
        gap = 5
        corner_radius = 8

        cell_width = (canvas_width - (cols + 1) * gap) / cols
        cell_height = (canvas_height - (rows + 1) * gap) / rows

        # Draw all squares as gray initially
        for r in range(rows):
            for c in range(cols):
                x1 = gap + c * (cell_width + gap)
                y1 = gap + r * (cell_height + gap)
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                self._create_rounded_rectangle(self.puzzle_canvas, x1, y1, x2, y2, radius=corner_radius, fill="#e0e0e0", outline="")

        # Draw green squares based on total_habits_this_week
        for i in range(min(total_habits_this_week, rows * cols)):
            row = i // cols
            col = i % cols
            x1 = gap + col * (cell_width + gap)
            y1 = gap + row * (cell_height + gap)
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            self._create_rounded_rectangle(self.puzzle_canvas, x1, y1, x2, y2, radius=corner_radius, fill="#4caf50", outline="")

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = HabitTracker(root)
    root.mainloop()
