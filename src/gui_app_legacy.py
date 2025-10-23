"""
GUI Application for Mouse Gesture Control
----------------------------------------
Provides a modern GUI interface for configuring and managing the gesture control system.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import threading
from typing import Dict, Any
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gesture_controller import GestureController
from input_listener import InputListener
from actions import perform_action


class GestureControlGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mouse Gesture Control")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        
        # Configuration
        self.config_path = "config.json"
        self.config = self.load_config()
        
        # Gesture control state
        self.gesture_controller = None
        self.input_listener = None
        self.gestures_enabled = False
        self.background_thread = None
        
        # Create GUI elements
        self.create_widgets()
        self.update_ui_from_config()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # Return default config
        return {
            "up": "task_view",
            "down": "close_task_view", 
            "left": "desktop_right",
            "right": "desktop_left",
            "debug": False,
            "threshold": 120.0,
            "cooldown": 0.5,
            "use_alt_instead_of_ctrl": True
        }
    
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            return False
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Mouse Gesture Control", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Gestures: Disabled", 
                                     font=("Arial", 10))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.toggle_button = ttk.Button(status_frame, text="Enable Gestures", 
                                       command=self.toggle_gestures)
        self.toggle_button.grid(row=0, column=1, padx=(10, 0))
        
        # Gesture mappings section
        mappings_frame = ttk.LabelFrame(main_frame, text="Gesture Mappings", padding="10")
        mappings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        mappings_frame.columnconfigure(1, weight=1)
        
        # Direction mappings
        directions = ["up", "down", "left", "right"]
        self.direction_vars = {}
        
        for i, direction in enumerate(directions):
            ttk.Label(mappings_frame, text=f"{direction.capitalize()}:").grid(
                row=i, column=0, sticky=tk.W, pady=2)
            
            var = tk.StringVar()
            self.direction_vars[direction] = var
            combo = ttk.Combobox(mappings_frame, textvariable=var, width=20, state="readonly")
            combo['values'] = ("task_view", "close_task_view", "desktop_left", "desktop_right")
            combo.grid(row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Threshold setting
        ttk.Label(settings_frame, text="Threshold (px):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.threshold_var = tk.DoubleVar()
        threshold_scale = ttk.Scale(settings_frame, from_=50, to=300, 
                                  variable=self.threshold_var, orient=tk.HORIZONTAL)
        threshold_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        self.threshold_label = ttk.Label(settings_frame, text="120")
        self.threshold_label.grid(row=0, column=2, padx=(5, 0))
        
        # Cooldown setting
        ttk.Label(settings_frame, text="Cooldown (s):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.cooldown_var = tk.DoubleVar()
        cooldown_scale = ttk.Scale(settings_frame, from_=0.1, to=2.0, 
                                  variable=self.cooldown_var, orient=tk.HORIZONTAL)
        cooldown_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        self.cooldown_label = ttk.Label(settings_frame, text="0.5")
        self.cooldown_label.grid(row=1, column=2, padx=(5, 0))
        
        # Debug mode
        self.debug_var = tk.BooleanVar()
        debug_check = ttk.Checkbutton(settings_frame, text="Debug Mode", 
                                     variable=self.debug_var)
        debug_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Alt instead of Ctrl
        self.alt_var = tk.BooleanVar()
        alt_check = ttk.Checkbutton(settings_frame, text="Use Alt instead of Ctrl", 
                                   variable=self.alt_var)
        alt_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Bind scale events
        threshold_scale.configure(command=self.update_threshold_label)
        cooldown_scale.configure(command=self.update_cooldown_label)
        
        # Buttons section
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Save Settings", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Reset to Defaults", 
                  command=self.reset_defaults).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Minimize to Tray", 
                  command=self.minimize_to_tray).pack(side=tk.LEFT, padx=5)
    
    def update_threshold_label(self, value):
        """Update threshold label when scale changes."""
        self.threshold_label.config(text=f"{float(value):.0f}")
    
    def update_cooldown_label(self, value):
        """Update cooldown label when scale changes."""
        self.cooldown_label.config(text=f"{float(value):.2f}")
    
    def update_ui_from_config(self):
        """Update UI elements from current configuration."""
        # Update direction mappings
        for direction, var in self.direction_vars.items():
            var.set(self.config.get(direction, ""))
        
        # Update settings
        self.threshold_var.set(self.config.get("threshold", 120.0))
        self.cooldown_var.set(self.config.get("cooldown", 0.5))
        self.debug_var.set(self.config.get("debug", False))
        self.alt_var.set(self.config.get("use_alt_instead_of_ctrl", True))
        
        # Update labels
        self.update_threshold_label(self.threshold_var.get())
        self.update_cooldown_label(self.cooldown_var.get())
    
    def toggle_gestures(self):
        """Toggle gesture detection on/off."""
        if self.gestures_enabled:
            self.disable_gestures()
        else:
            self.enable_gestures()
    
    def enable_gestures(self):
        """Enable gesture detection."""
        try:
            # Create gesture controller
            self.gesture_controller = GestureController(
                threshold=self.config.get("threshold", 120.0),
                cooldown=self.config.get("cooldown", 0.5)
            )
            
            # Create input listener
            self.input_listener = InputListener(
                on_both_press=self.on_both_press,
                on_move=self.on_move,
                on_release=self.on_release
            )
            
            # Start listening in background thread
            self.background_thread = threading.Thread(target=self.start_listening, daemon=True)
            self.background_thread.start()
            
            self.gestures_enabled = True
            self.status_label.config(text="Gestures: Enabled", foreground="green")
            self.toggle_button.config(text="Disable Gestures")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enable gestures: {e}")
    
    def disable_gestures(self):
        """Disable gesture detection."""
        if self.input_listener:
            try:
                self.input_listener.listener.stop()
            except:
                pass
        
        self.gestures_enabled = False
        self.status_label.config(text="Gestures: Disabled", foreground="red")
        self.toggle_button.config(text="Enable Gestures")
    
    def start_listening(self):
        """Start the input listener."""
        if self.input_listener:
            self.input_listener.start()
    
    def on_both_press(self, x, y):
        """Handle both mouse buttons pressed."""
        if self.gesture_controller:
            self.gesture_controller.start_gesture(x, y)
    
    def on_move(self, x, y):
        """Handle mouse movement during gesture."""
        if not self.gesture_controller:
            return
            
        direction = self.gesture_controller.detect_direction(x, y)
        if direction:
            action = self.config.get(direction)
            if action:
                perform_action(
                    action,
                    debug=self.config.get("debug", False),
                    direction=direction,
                    use_alt=self.config.get("use_alt_instead_of_ctrl", True)
                )
            self.gesture_controller.end_gesture()
    
    def on_release(self):
        """Handle mouse button release."""
        if self.gesture_controller:
            self.gesture_controller.end_gesture()
    
    def save_settings(self):
        """Save current settings to configuration."""
        # Update config from UI
        for direction, var in self.direction_vars.items():
            self.config[direction] = var.get()
        
        self.config["threshold"] = self.threshold_var.get()
        self.config["cooldown"] = self.cooldown_var.get()
        self.config["debug"] = self.debug_var.get()
        self.config["use_alt_instead_of_ctrl"] = self.alt_var.get()
        
        # Save to file
        if self.save_config():
            messagebox.showinfo("Success", "Settings saved successfully!")
            
            # Restart gesture detection if enabled
            if self.gestures_enabled:
                self.disable_gestures()
                self.enable_gestures()
    
    def reset_defaults(self):
        """Reset settings to default values."""
        if messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            self.config = {
                "up": "task_view",
                "down": "close_task_view",
                "left": "desktop_right", 
                "right": "desktop_left",
                "debug": False,
                "threshold": 120.0,
                "cooldown": 0.5,
                "use_alt_instead_of_ctrl": True
            }
            self.update_ui_from_config()
    
    def minimize_to_tray(self):
        """Minimize window to system tray."""
        self.root.withdraw()
        # Note: Tray functionality will be implemented in the main application
    
    def on_closing(self):
        """Handle window closing."""
        self.disable_gestures()
        self.root.destroy()
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


if __name__ == "__main__":
    app = GestureControlGUI()
    app.run()
