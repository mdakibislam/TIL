import math
import tkinter as tk
from tkinter import messagebox

class Dynamic3DGraphApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Universal Dynamic 3D Grapher")
        self.root.configure(bg="#1e1e1e")

        # Initial viewing angles & default scale
        self.elevation = 0.5
        self.azimuth = 0.785
        self.zoom = 1.0

        # Mouse tracking for rotation
        self.last_x = 0
        self.last_y = 0
        self.grid_data = []

        # --- UI LAYOUT ---
        # Left Panel for Settings & Custom Variables
        self.control_panel = tk.Frame(root, bg="#252526", width=280)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.control_panel.pack_propagate(False)

        # Right Panel for Canvas
        self.canvas_panel = tk.Frame(root, bg="#1e1e1e")
        self.canvas_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            self.canvas_panel,
            width=700,
            height=650,
            bg="#121212",
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Bind Interaction Controls
        self.canvas.bind("<Button-1>", self.start_rotate)
        self.canvas.bind("<B1-Motion>", self.rotate)
        self.canvas.bind("<MouseWheel>", self.handle_zoom)  # Windows zoom
        self.canvas.bind("<Button-4>", self.handle_zoom)  # Linux scroll up
        self.canvas.bind("<Button-5>", self.handle_zoom)  # Linux scroll down

        # --- BUILD CONTROL PANEL INPUTS ---
        self.create_input_fields()

        # Build initial graph
        self.update_graph()

    def create_input_fields(self):
        """Generates the customizable user inputs on the fly."""
        style = {"bg": "#252526", "fg": "white", "font": ("Arial", 10)}
        entry_style = {
            "bg": "#3e3e42",
            "fg": "white",
            "insertbackground": "white",
            "relief": "flat",
            "font": ("Arial", 10),
        }

        # Title
        tk.Label(
            self.control_panel,
            text="⚙️ Graph Configuration",
            font=("Arial", 12, "bold"),
            bg="#252526",
            fg="#007acc",
        ).pack(pady=10)

        # 1. Equation Field
        tk.Label(
            self.control_panel, text="3D Equation f(x, y):", **style
        ).pack(anchor="w", padx=10, pady=(5, 0))  # <-- FIXED TYPO HERE (changed px to padx)
        
        self.eqn_entry = tk.Entry(self.control_panel, **entry_style)
        self.eqn_entry.insert(
            0, "sin(sqrt(x**2 + y**2)) / (sqrt(x**2 + y**2) + 0.1)"
        )
        self.eqn_entry.pack(fill=tk.X, padx=10, pady=2)

        # Help hint for equations
        tk.Label(
            self.control_panel,
            text="Use standard python math like: sin, cos, tan, sqrt, pi, e, **",
            font=("Arial", 8, "italic"),
            bg="#252526",
            fg="#888888",
            wraplength=240,
        ).pack(anchor="w", padx=10, pady=(0, 5))

        # 2. Custom Variables (User can declare a, b, c to use in equation)
        tk.Label(
            self.control_panel,
            text="Custom Constants (Optional):\nFormat: a=2; b=0.5; c=10",
            **style,
        ).pack(anchor="w", padx=10, pady=(5, 0))
        self.vars_entry = tk.Entry(self.control_panel, **entry_style)
        self.vars_entry.insert(0, "a=1.0; b=1.0")
        self.vars_entry.pack(fill=tk.X, padx=10, pady=2)

        # 3. Grid Resolution
        tk.Label(
            self.control_panel, text="Resolution (Grid Lines):", **style
        ).pack(anchor="w", padx=10, pady=(5, 0))
        self.res_entry = tk.Entry(self.control_panel, **entry_style)
        self.res_entry.insert(0, "30")
        self.res_entry.pack(fill=tk.X, padx=10, pady=2)

        # 4. Math Bounds (X min/max, Y min/max)
        bounds_frame = tk.Frame(self.control_panel, bg="#252526")
        bounds_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(bounds_frame, text="X Min", **style).grid(row=0, column=0)
        self.xmin_entry = tk.Entry(bounds_frame, width=8, **entry_style)
        self.xmin_entry.insert(0, "-5.0")
        self.xmin_entry.grid(row=0, column=1, padx=2)

        tk.Label(bounds_frame, text="X Max", **style).grid(row=0, column=2)
        self.xmax_entry = tk.Entry(bounds_frame, width=8, **entry_style)
        self.xmax_entry.insert(0, "5.0")
        self.xmax_entry.grid(row=0, column=3, padx=2)

        tk.Label(bounds_frame, text="Y Min", **style).grid(row=1, column=0, pady=5)
        self.ymin_entry = tk.Entry(bounds_frame, width=8, **entry_style)
        self.ymin_entry.insert(0, "-5.0")
        self.ymin_entry.grid(row=1, column=1, padx=2, pady=5)

        tk.Label(bounds_frame, text="Y Max", **style).grid(row=1, column=2, pady=5)
        self.ymax_entry = tk.Entry(bounds_frame, width=8, **entry_style)
        self.ymax_entry.insert(0, "5.0")
        self.ymax_entry.grid(row=1, column=3, padx=2, pady=5)

        # Height visual scaling
        tk.Label(self.control_panel, text="Z Height Scale:", **style).pack(
            anchor="w", padx=10, pady=(5, 0)
        )
        self.zscale_entry = tk.Entry(self.control_panel, **entry_style)
        self.zscale_entry.insert(0, "120")
        self.zscale_entry.pack(fill=tk.X, padx=10, pady=2)

        # Color Theme Selection
        tk.Label(self.control_panel, text="Color Scheme:", **style).pack(
            anchor="w", padx=10, pady=(5, 0)
        )
        self.color_var = tk.StringVar(value="Neon Ripple")
        themes = ["Neon Ripple", "Volcano Fire", "Emerald Glaze", "Cyberpunk Grid"]
        self.theme_menu = tk.OptionMenu(
            self.control_panel, self.color_var, *themes
        )
        self.theme_menu.config(
            bg="#3e3e42", fg="white", highlightthickness=0, relief="flat"
        )
        self.theme_menu["menu"].config(bg="#3e3e42", fg="white")
        self.theme_menu.pack(fill=tk.X, padx=10, pady=5)

        # ACTION BUTTONS
        self.btn_update = tk.Button(
            self.control_panel,
            text="🔄 Render / Update Graph",
            command=self.update_graph,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
        )
        self.btn_update.pack(fill=tk.X, padx=10, pady=(20, 5))

        self.btn_shot = tk.Button(
            self.control_panel,
            text="📸 Take Angle Shot",
            command=self.take_shot,
            bg="#007acc",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
        )
        self.btn_shot.pack(fill=tk.X, padx=10, pady=5)

    # 2. DYNAMIC EQUATION PARSER & CALCULATOR
    def calculate_z(self, x, y, expr_str, local_vars):
        """Evaluates math safely without needing external parsing modules."""
        # Inject standard math names into evaluation environment
        safe_env = {
            "x": x,
            "y": y,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e,
            "exp": math.exp,
            "log": math.log,
            "abs": abs,
        }
        # Inject the custom variables declared by the user
        safe_env.update(local_vars)
        try:
            return float(eval(expr_str, {"__builtins__": None}, safe_env))
        except:
            return 0.0  # Handle mathematical undefined zones seamlessly

    def update_graph(self):
        """Reads configuration entries dynamically, computes coordinates, and redraws."""
        try:
            # Parse user variables
            local_vars = {}
            var_raw = self.vars_entry.get().strip()
            if var_raw:
                for statement in var_raw.split(";"):
                    if "=" in statement:
                        k, v = statement.split("=")
                        local_vars[k.strip()] = float(v.strip())

            # Read limits & rules
            expr = self.eqn_entry.get()
            grid_size = int(self.res_entry.get())
            x_min, x_max = float(self.xmin_entry.get()), float(self.xmax_entry.get())
            y_min, y_max = float(self.ymin_entry.get()), float(self.ymax_entry.get())
            self.z_scale = float(self.zscale_entry.get())

            # Generate grid array
            x_vals = [x_min + (x_max - x_min) * i / (grid_size - 1) for i in range(grid_size)]
            y_vals = [y_min + (y_max - y_min) * j / (grid_size - 1) for j in range(grid_size)]

            self.grid_data = []
            self.min_z, self.max_z = float("inf"), float("-inf")

            for x in x_vals:
                row = []
                for y in y_vals:
                    z = self.calculate_z(x, y, expr, local_vars)
                    if z < self.min_z: self.min_z = z
                    if z > self.max_z: self.max_z = z
                    row.append((x * 40, y * 40, z))
                self.grid_data.append(row)

            self.render_graph()

        except Exception as e:
            messagebox.showerror("Configuration Error", f"Invalid math formula or parameter setup:\n{str(e)}")

    

    def project_3d_to_2d(self, x, y, z):
        cx = self.canvas.winfo_width() / 2 if self.canvas.winfo_width() > 10 else 350
        cy = self.canvas.winfo_height() / 2 if self.canvas.winfo_height() > 10 else 325

        # Apply Zoom & Scale settings
        x, y, z = x * self.zoom, y * self.zoom, z * self.z_scale * self.zoom

        # 3D Matrix Rotations
        x1 = x * math.cos(self.azimuth) - y * math.sin(self.azimuth)
        y1 = x * math.sin(self.azimuth) + y * math.cos(self.azimuth)
        z2 = z * math.cos(self.elevation) - y1 * math.sin(self.elevation)

        return int(x1 + cx), int(-z2 + cy)

    def render_graph(self):
        self.canvas.delete("all")
        if not self.grid_data: return

        grid_size = len(self.grid_data)
        theme = self.color_var.get()

        # Render mesh connectors
        for i in range(grid_size):
            for j in range(grid_size):
                curr_z = self.grid_data[i][j][2]
                z_range = (self.max_z - self.min_z) if (self.max_z - self.min_z) != 0 else 1.0
                ratio = (curr_z - self.min_z) / z_range

                color = self.get_theme_color(ratio, theme)

                # Connect horizontally
                if i < grid_size - 1:
                    x1, y1 = self.project_3d_to_2d(*self.grid_data[i][j])
                    x2, y2 = self.project_3d_to_2d(*self.grid_data[i + 1][j])
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

                # Connect vertically
                if j < grid_size - 1:
                    x1, y1 = self.project_3d_to_2d(*self.grid_data[i][j])
                    x2, y2 = self.project_3d_to_2d(*self.grid_data[i][j + 1])
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

        # Helper Instruction Label
        self.canvas.create_text(
            20, 20, text="🖱️ Drag Left-Click to Rotate  |  Scroll Wheel to Zoom",
            fill="#777777", anchor="w", font=("Arial", 9)
        )

    def get_theme_color(self, ratio, theme):
        ratio = max(0.0, min(1.0, ratio))
        if theme == "Volcano Fire":
            r, g, b = int(120 + 135 * ratio), int(20 * ratio), int(30 * (1 - ratio))
        elif theme == "Emerald Glaze":
            r, g, b = int(10 * ratio), int(100 + 155 * ratio), int(120 * ratio)
        elif theme == "Cyberpunk Grid":
            r, g, b = int(255 * ratio), int(0), int(255 * (1 - ratio))
        else:  # Neon Ripple (Default Blue -> Orange)
            r, g, b = int(255 * ratio), int(100 + 100 * ratio), int(255 * (1 - ratio))
        return f"#{r:02x}{g:02x}{b:02x}"

    # 4. CONTROLS & CAPTURE
    def start_rotate(self, event):
        self.last_x, self.last_y = event.x, event.y

    def rotate(self, event):
        self.azimuth += (event.x - self.last_x) * 0.007
        self.elevation += (event.y - self.last_y) * 0.007
        self.last_x, self.last_y = event.x, event.y
        self.render_graph()

    def handle_zoom(self, event):
        if event.num == 4 or event.delta > 0:
            self.zoom *= 1.1
        elif event.num == 5 or event.delta < 0:
            self.zoom *= 0.9
        self.render_graph()

    def take_shot(self):
        filename = f"custom_graph_shot_{int(math.degrees(self.elevation))}_{int(math.degrees(self.azimuth))}.ps"
        self.canvas.postscript(file=filename, colormode="color")
        messagebox.showinfo("Shot Saved", f"Saved canvas frame successfully to workspace as:\n'{filename}'")


# Main execution context
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1020x680")
    app = Dynamic3DGraphApp(root)
    root.mainloop()