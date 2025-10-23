#!/usr/bin/env python3
"""
Mouse Gesture Control - GUI Launcher
====================================
Launches the GUI application with system tray support.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    try:
        from src.main_gui import MouseGestureControlApp
        app = MouseGestureControlApp()
        app.run()
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("Please install required dependencies:")
        print("pip install pynput keyboard pystray Pillow")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
