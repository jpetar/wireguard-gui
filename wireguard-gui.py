#!/usr/bin/env python3
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

CONFIG_DIR = "/etc/wireguard"
HISTORY_FILE = os.path.expanduser("~/.wg_gui_last")
CUSTOM_CONFIGS_FILE = os.path.expanduser("~/.wg_gui_custom_configs")

# Color scheme - Modern dark theme
COLORS = {
    "bg": "#0d1117",
    "bg_light": "#161b22",
    "surface": "#1c2128",
    "surface_light": "#262c36",
    "border": "#30363d",
    "fg": "#e6edf3",
    "fg_muted": "#7d8590",
    "accent": "#58a6ff",
    "success": "#3fb950",
    "danger": "#f85149",
    "warning": "#d29922",
    "output_bg": "#0d1117",
    "button_hover": "#2d333b",
}

def run_cmd(cmd):
    """Run shell command and return output or error."""
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return out
    except subprocess.CalledProcessError as e:
        return e.output

class WireGuardGUI:
    def __init__(self, root):
        self.root = root
        root.title("🔐 WireGuard Manager")
        root.configure(bg=COLORS["bg"])
        root.geometry("1100x750")
        root.minsize(900, 600)

        # Configure styles
        self.setup_styles()

        self.interface_var = tk.StringVar()
        self.interface_var.trace_add("write", self.on_interface_change)

        # Main container
        main_container = tk.Frame(root, bg=COLORS["bg"])
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # --- Header ---
        header = tk.Frame(main_container, bg=COLORS["bg"])
        header.pack(fill="x", pady=(0, 20))

        title_label = tk.Label(
            header,
            text="🔐 WireGuard Manager",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["fg"]
        )
        title_label.pack(side="left")

        # Status indicator with background
        self.status_frame = tk.Frame(
            header,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        self.status_frame.pack(side="right")

        status_inner = tk.Frame(self.status_frame, bg=COLORS["surface"])
        status_inner.pack(padx=15, pady=8)

        self.status_indicator = tk.Label(
            status_inner,
            text="●",
            font=("Arial", 14),
            bg=COLORS["surface"],
            fg=COLORS["surface_light"]
        )
        self.status_indicator.pack(side="left", padx=(0, 8))

        self.status_label = tk.Label(
            status_inner,
            text="Disconnected",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["surface"],
            fg=COLORS["fg"]
        )
        self.status_label.pack(side="left")

        # --- Interface Selection Card ---
        select_card = tk.Frame(
            main_container,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            relief="flat"
        )
        select_card.pack(fill="x", pady=(0, 15))

        select_inner = tk.Frame(select_card, bg=COLORS["surface"])
        select_inner.pack(fill="x", padx=20, pady=15)

        label = tk.Label(
            select_inner,
            text="Interface:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["surface"],
            fg=COLORS["fg"]
        )
        label.pack(side="left", padx=(0, 10))

        self.interface_dropdown = ttk.Combobox(
            select_inner,
            textvariable=self.interface_var,
            width=35,
            font=("Segoe UI", 10),
            style="Custom.TCombobox"
        )
        self.interface_dropdown.pack(side="left", padx=5)

        ttk.Button(
            select_inner,
            text="🔄 Reload",
            command=self.load_interfaces,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            select_inner,
            text="📁 Browse Config",
            command=self.choose_config,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        # --- Control Buttons Card ---
        control_card = tk.Frame(
            main_container,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            relief="flat"
        )
        control_card.pack(fill="x", pady=(0, 15))

        control_inner = tk.Frame(control_card, bg=COLORS["surface"])
        control_inner.pack(fill="x", padx=20, pady=18)

        # Connection controls
        conn_label = tk.Label(
            control_inner,
            text="Connection:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["surface"],
            fg=COLORS["fg"]
        )
        conn_label.grid(row=0, column=0, sticky="w", pady=(0, 8))

        conn_frame = tk.Frame(control_inner, bg=COLORS["surface"])
        conn_frame.grid(row=1, column=0, sticky="w", pady=(0, 15))

        ttk.Button(
            conn_frame,
            text="▲ Connect",
            command=self.ifup,
            style="Success.TButton",
            width=15
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            conn_frame,
            text="▼ Disconnect",
            command=self.ifdown,
            style="Danger.TButton",
            width=15
        ).pack(side="left")

        # Info controls
        info_label = tk.Label(
            control_inner,
            text="Information:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["surface"],
            fg=COLORS["fg"]
        )
        info_label.grid(row=2, column=0, sticky="w", pady=(0, 8))

        info_frame = tk.Frame(control_inner, bg=COLORS["surface"])
        info_frame.grid(row=3, column=0, sticky="w", pady=(0, 15))

        ttk.Button(
            info_frame,
            text="📊 Show Status",
            command=self.show_wg,
            style="Info.TButton",
            width=15
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            info_frame,
            text="📋 Quick Status",
            command=self.show_status,
            style="Info.TButton",
            width=15
        ).pack(side="left")

        # Config controls
        config_label = tk.Label(
            control_inner,
            text="Configuration:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["surface"],
            fg=COLORS["fg"]
        )
        config_label.grid(row=4, column=0, sticky="w", pady=(0, 8))

        config_frame = tk.Frame(control_inner, bg=COLORS["surface"])
        config_frame.grid(row=5, column=0, sticky="w")

        ttk.Button(
            config_frame,
            text="✏️  Edit Config",
            command=self.edit_config,
            style="Warning.TButton",
            width=15
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            config_frame,
            text="💾 Save Config",
            command=self.save_config,
            style="Warning.TButton",
            width=15
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            config_frame,
            text="🔧 Strip Config",
            command=self.strip_config,
            style="Warning.TButton",
            width=15
        ).pack(side="left")

        # --- Output Card ---
        output_card = tk.Frame(
            main_container,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            relief="flat"
        )
        output_card.pack(fill="both", expand=True)

        output_header = tk.Frame(output_card, bg=COLORS["bg_light"])
        output_header.pack(fill="x")

        output_title = tk.Label(
            output_header,
            text="📟 Output",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_light"],
            fg=COLORS["fg"]
        )
        output_title.pack(side="left", padx=20, pady=10)

        ttk.Button(
            output_header,
            text="🗑️  Clear",
            command=lambda: self.output.delete("1.0", tk.END),
            style="Small.TButton"
        ).pack(side="right", padx=20, pady=8)

        # Output text area container
        output_container = tk.Frame(output_card, bg=COLORS["output_bg"])
        output_container.pack(fill="both", expand=True, padx=2, pady=2)

        self.output = scrolledtext.ScrolledText(
            output_container,
            width=90,
            height=20,
            font=("JetBrains Mono", 9),
            bg=COLORS["output_bg"],
            fg=COLORS["fg"],
            insertbackground=COLORS["accent"],
            selectbackground=COLORS["surface_light"],
            selectforeground=COLORS["fg"],
            relief="flat",
            padx=15,
            pady=12,
            wrap="word"
        )
        self.output.pack(fill="both", expand=True)

        # Load initial interface list
        self.load_interfaces()

        # Restore last-used interface
        self.restore_last_interface()

        # Initial status check
        self.update_status()

    def setup_styles(self):
        """Configure custom ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        # Base button
        style.configure(
            "TButton",
            font=("Segoe UI", 9),
            background=COLORS["surface_light"],
            foreground=COLORS["fg"],
            borderwidth=1,
            focuscolor=COLORS["accent"],
            lightcolor=COLORS["surface_light"],
            darkcolor=COLORS["surface_light"],
            relief="flat",
            padding=(12, 8)
        )
        style.map("TButton",
            background=[("active", COLORS["button_hover"])],
            relief=[("pressed", "flat")]
        )

        # Accent buttons (Reload, Browse)
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 9),
            background=COLORS["accent"],
            foreground="#ffffff",
            borderwidth=0,
            relief="flat",
            padding=(12, 8)
        )
        style.map("Accent.TButton",
            background=[("active", "#6cb6ff")],
            relief=[("pressed", "flat")]
        )

        # Success button (Connect)
        style.configure(
            "Success.TButton",
            font=("Segoe UI", 10, "bold"),
            background=COLORS["success"],
            foreground="#ffffff",
            borderwidth=0,
            relief="flat",
            padding=(20, 10)
        )
        style.map("Success.TButton",
            background=[("active", "#4cc961")],
            relief=[("pressed", "flat")]
        )

        # Danger button (Disconnect)
        style.configure(
            "Danger.TButton",
            font=("Segoe UI", 10, "bold"),
            background=COLORS["danger"],
            foreground="#ffffff",
            borderwidth=0,
            relief="flat",
            padding=(20, 10)
        )
        style.map("Danger.TButton",
            background=[("active", "#ff6b6b")],
            relief=[("pressed", "flat")]
        )

        # Info buttons
        style.configure(
            "Info.TButton",
            font=("Segoe UI", 9),
            background=COLORS["surface_light"],
            foreground=COLORS["fg"],
            borderwidth=1,
            bordercolor=COLORS["border"],
            relief="flat",
            padding=(12, 8)
        )
        style.map("Info.TButton",
            background=[("active", COLORS["button_hover"])],
            relief=[("pressed", "flat")]
        )

        # Warning buttons
        style.configure(
            "Warning.TButton",
            font=("Segoe UI", 9),
            background=COLORS["surface_light"],
            foreground=COLORS["fg"],
            borderwidth=1,
            bordercolor=COLORS["border"],
            relief="flat",
            padding=(12, 8)
        )
        style.map("Warning.TButton",
            background=[("active", COLORS["button_hover"])],
            relief=[("pressed", "flat")]
        )

        # Small button (Clear)
        style.configure(
            "Small.TButton",
            font=("Segoe UI", 8),
            background=COLORS["surface"],
            foreground=COLORS["fg_muted"],
            borderwidth=0,
            relief="flat",
            padding=(10, 5)
        )
        style.map("Small.TButton",
            background=[("active", COLORS["button_hover"])],
            relief=[("pressed", "flat")]
        )

        # Combobox
        style.configure(
            "Custom.TCombobox",
            fieldbackground=COLORS["surface_light"],
            background=COLORS["surface_light"],
            foreground=COLORS["fg"],
            arrowcolor=COLORS["fg"],
            borderwidth=1,
            relief="flat"
        )
        style.map("Custom.TCombobox",
            fieldbackground=[("readonly", COLORS["surface_light"])],
            selectbackground=[("readonly", COLORS["surface_light"])],
            selectforeground=[("readonly", COLORS["fg"])]
        )

    def on_interface_change(self, *args):
        """Called when interface selection changes."""
        self.update_status()

    def update_status(self):
        """Update the connection status indicator."""
        iface = self.interface_var.get()
        if not iface:
            self.status_indicator.config(fg=COLORS["surface_light"])
            self.status_label.config(text="No interface selected")
            return

        # Check if interface is active
        try:
            result = subprocess.check_output(["wg", "show"], text=True, stderr=subprocess.DEVNULL)
            # Extract just the interface name if it's a path
            iface_name = os.path.basename(iface).replace(".conf", "") if "/" in iface else iface

            if iface_name in result:
                self.status_indicator.config(fg=COLORS["success"])
                self.status_label.config(text="Connected")
            else:
                self.status_indicator.config(fg=COLORS["danger"])
                self.status_label.config(text="Disconnected")
        except:
            self.status_indicator.config(fg=COLORS["surface_light"])
            self.status_label.config(text="Unknown")

    # ---------------------------
    # Interface loading
    # ---------------------------
    def load_interfaces(self):
        interfaces = []

        # Load standard interfaces from CONFIG_DIR
        if os.path.isdir(CONFIG_DIR):
            for f in os.listdir(CONFIG_DIR):
                if f.endswith(".conf"):
                    interfaces.append(f.replace(".conf", ""))

        # Load custom config paths from saved file
        custom_configs = self.load_custom_configs()
        interfaces.extend(custom_configs)

        self.interface_dropdown["values"] = interfaces
        if interfaces and not self.interface_var.get():
            self.interface_var.set(interfaces[0])

        self.save_last_interface()

    def choose_config(self):
        """Allow user to select a config file anywhere on the filesystem."""
        initialdir = CONFIG_DIR if os.path.isdir(CONFIG_DIR) else os.path.expanduser("~")
        path = filedialog.askopenfilename(
            title="Select WireGuard config",
            initialdir=initialdir,
            filetypes=[("WireGuard config", "*.conf"), ("All files", "*.*")],
        )
        if not path:
            return

        # Set the interface_var to the full config path
        self.interface_var.set(path)

        # Add to dropdown values if not already present
        values = list(self.interface_dropdown["values"])
        if path not in values:
            values.append(path)
            self.interface_dropdown["values"] = values

        # Save both the interface and update the custom configs list
        self.save_custom_config(path)
        self.save_last_interface()

    def get_if(self):
        iface = self.interface_var.get()
        if not iface:
            messagebox.showerror("Error", "No interface selected.")
            return None
        self.save_last_interface()
        return iface

    # ---------------------------
    # History persistence
    # ---------------------------
    def save_last_interface(self):
        try:
            with open(HISTORY_FILE, "w") as f:
                f.write(self.interface_var.get())
        except:
            pass

    def restore_last_interface(self):
        if os.path.exists(HISTORY_FILE):
            try:
                content = open(HISTORY_FILE).read().strip()
                self.interface_var.set(content)
            except:
                pass

    def load_custom_configs(self):
        """Load list of custom config file paths."""
        if not os.path.exists(CUSTOM_CONFIGS_FILE):
            return []

        try:
            with open(CUSTOM_CONFIGS_FILE, "r") as f:
                configs = [line.strip() for line in f if line.strip()]
            # Filter out configs that no longer exist
            return [cfg for cfg in configs if os.path.exists(cfg)]
        except:
            return []

    def save_custom_config(self, config_path):
        """Save a custom config path to the persistent list."""
        try:
            # Load existing configs
            existing_configs = self.load_custom_configs()

            # Add new config if not already present
            if config_path not in existing_configs:
                existing_configs.append(config_path)

            # Save back to file
            with open(CUSTOM_CONFIGS_FILE, "w") as f:
                for cfg in existing_configs:
                    f.write(cfg + "\n")
        except:
            pass

    # ---------------------------
    # Output helpers
    # ---------------------------
    def show_output(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    # ---------------------------
    # Helper: resolve config path
    # ---------------------------
    def _resolve_conf_path(self, iface):
        """
        If iface looks like a path to a config file and it exists, use it.
        Otherwise, treat iface as an interface name in CONFIG_DIR.
        """
        # If iface is an absolute path or contains a path separator and points to an existing file
        if (os.path.isabs(iface) or os.path.sep in iface) and os.path.exists(iface):
            return iface

        # Otherwise, assume CONFIG_DIR/<iface>.conf
        conf_path = os.path.join(CONFIG_DIR, iface + ".conf")
        return conf_path

    # ---------------------------
    # WireGuard commands
    # ---------------------------
    def show_wg(self):
        out = run_cmd(["wg"])
        self.show_output(out)

    def show_status(self):
        out = run_cmd(["wg-quick", "status"])
        self.show_output(out)

    def ifup(self):
        iface = self.get_if()
        if iface:
            # wg-quick accepts either interface name or full config path
            out = run_cmd(["sudo", "wg-quick", "up", iface])
            self.show_output(out)
            self.update_status()

    def ifdown(self):
        iface = self.get_if()
        if iface:
            out = run_cmd(["sudo", "wg-quick", "down", iface])
            self.show_output(out)
            self.update_status()

    def save_config(self):
        iface = self.get_if()
        if iface:
            out = run_cmd(["sudo", "wg-quick", "save", iface])
            self.show_output(out)

    def strip_config(self):
        iface = self.get_if()
        if iface:
            out = run_cmd(["sudo", "wg-quick", "strip", iface])
            self.show_output(out)

    def edit_config(self):
        iface = self.get_if()
        if not iface:
            return

        conf_path = self._resolve_conf_path(iface)

        if not os.path.exists(conf_path):
            messagebox.showerror("Error", "%s does not exist." % conf_path)
            return

        editor = tk.Toplevel(self.root)
        editor.title("✏️  Editing %s" % os.path.basename(conf_path))
        editor.configure(bg=COLORS["bg"])
        editor.geometry("900x650")

        # Header
        header = tk.Frame(editor, bg=COLORS["bg_light"])
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="✏️  Configuration Editor",
            font=("Segoe UI", 14, "bold"),
            bg=COLORS["bg_light"],
            fg=COLORS["fg"]
        )
        title.pack(side="left", padx=20, pady=12)

        subtitle = tk.Label(
            header,
            text=conf_path,
            font=("Segoe UI", 9),
            bg=COLORS["bg_light"],
            fg=COLORS["fg_muted"]
        )
        subtitle.pack(side="left", padx=5, pady=12)

        # Editor area with border
        editor_outer = tk.Frame(
            editor,
            bg=COLORS["bg"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        editor_outer.pack(fill="both", expand=True, padx=15, pady=15)

        text = scrolledtext.ScrolledText(
            editor_outer,
            width=90,
            height=28,
            font=("JetBrains Mono", 10),
            bg=COLORS["output_bg"],
            fg=COLORS["fg"],
            insertbackground=COLORS["accent"],
            selectbackground=COLORS["surface_light"],
            selectforeground=COLORS["fg"],
            relief="flat",
            padx=15,
            pady=12
        )
        text.pack(fill="both", expand=True, padx=1, pady=1)

        # Load file
        with open(conf_path) as f:
            text.insert(tk.END, f.read())

        # Button frame
        button_frame = tk.Frame(editor, bg=COLORS["bg"])
        button_frame.pack(fill="x", padx=15, pady=(0, 15))

        def save_changes():
            content = text.get("1.0", tk.END)
            try:
                with open(conf_path, "w") as f:
                    f.write(content)
                messagebox.showinfo("✓ Saved", "Configuration saved successfully!")
                editor.destroy()
            except PermissionError:
                messagebox.showerror("Error", "Permission denied. Run as root or use sudo.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(
            button_frame,
            text="💾 Save & Close",
            command=save_changes,
            style="Success.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="✖ Cancel",
            command=editor.destroy,
            style="Danger.TButton"
        ).pack(side="left", padx=5)

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = WireGuardGUI(root)
    root.mainloop()
