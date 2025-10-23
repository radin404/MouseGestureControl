#!/usr/bin/env python3
"""
Startup Launcher for Mouse Gesture Control
=========================================
Detects if the application should start minimized (for Windows startup).
"""

import sys
import os
import time

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main startup function."""
    # Check if we're starting from Windows startup
    # This can be detected by checking command line arguments or environment
    start_minimized = False
    
    # Check for startup arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--startup":
        start_minimized = True
    
    # Check if we're running from startup folder (common pattern)
    if "--startup" in sys.argv or "startup" in str(sys.argv).lower():
        start_minimized = True
    
    # Check if we're running from a startup context
    # (This is a simple heuristic - in practice, the installer will set this up)
    try:
        from src.main_gui import MouseGestureControlApp
        app = MouseGestureControlApp()
        app.run(start_minimized=start_minimized)
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("Please install required dependencies:")
        print("pip install pynput keyboard pystray Pillow")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
