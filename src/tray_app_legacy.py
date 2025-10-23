"""
System Tray Application for Mouse Gesture Control
-------------------------------------------------
Provides a system tray interface for the gesture control application.
"""

import pystray
from PIL import Image, ImageDraw
import threading
import sys
import os
import json
import time
from typing import Optional

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gesture_controller import GestureController
from input_listener import InputListener
from actions import perform_action


class GestureTrayApp:
    def __init__(self):
        self.config_path = "config.json"
        self.config = self.load_config()
        
        # Gesture control state
        self.gesture_controller = None
        self.input_listener = None
        self.gestures_enabled = False
        self.background_thread = None
        
        # GUI reference (will be set when GUI is created)
        self.gui_window = None
        
        # Create tray icon
        self.icon = self.create_tray_icon()
    
    def load_config(self) -> dict:
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
    
    def create_tray_icon(self):
        """Create the system tray icon."""
        # Create a simple icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        dc = ImageDraw.Draw(image)
        
        # Draw a simple mouse icon
        dc.ellipse([10, 10, 54, 54], fill='black', outline='gray', width=2)
        dc.ellipse([20, 20, 44, 44], fill='white')
        
        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem("Show Settings", self.show_settings),
            pystray.MenuItem("Enable Gestures", self.toggle_gestures, 
                           checked=lambda item: self.gestures_enabled),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.quit_app)
        )
        
        return pystray.Icon("MouseGestureControl", image, "Mouse Gesture Control", menu)
    
    def show_settings(self, icon=None, item=None):
        """Show the settings window."""
        if self.gui_window is None:
            # Import and create GUI window
            from gui_app import GestureControlGUI
            self.gui_window = GestureControlGUI()
            # Set up the tray reference in the GUI
            self.gui_window.tray_app = self
        
        # Show the window
        self.gui_window.root.deiconify()
        self.gui_window.root.lift()
        self.gui_window.root.focus_force()
    
    def toggle_gestures(self, icon=None, item=None):
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
            print("✅ Gestures enabled")
            
        except Exception as e:
            print(f"❌ Failed to enable gestures: {e}")
    
    def disable_gestures(self):
        """Disable gesture detection."""
        if self.input_listener:
            try:
                self.input_listener.listener.stop()
            except:
                pass
        
        self.gestures_enabled = False
        print("❌ Gestures disabled")
    
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
    
    def quit_app(self, icon=None, item=None):
        """Quit the application."""
        self.disable_gestures()
        if self.gui_window:
            self.gui_window.root.quit()
        self.icon.stop()
    
    def run(self):
        """Start the tray application."""
        print("🎧 Mouse Gesture Control - Starting tray application...")
        print("Right-click the tray icon for options.")
        
        # Start with gestures enabled by default
        self.enable_gestures()
        
        # Run the tray icon
        self.icon.run()


if __name__ == "__main__":
    app = GestureTrayApp()
    app.run()
