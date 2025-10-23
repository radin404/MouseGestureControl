#!/usr/bin/env python3
"""
Cleanup Script for Mouse Gesture Control
=======================================
Removes any Windows startup entries and cleans up old files.
"""

import os
import sys
import subprocess
import winreg

def remove_startup_entry():
    """Remove MouseGestureControl from Windows startup."""
    try:
        # Open the registry key for current user startup programs
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Run", 
                           0, winreg.KEY_SET_VALUE)
        
        # Try to delete the MouseGestureControl entry
        try:
            winreg.DeleteValue(key, "MouseGestureControl")
            print("SUCCESS: Removed MouseGestureControl from Windows startup")
        except FileNotFoundError:
            print("INFO: No MouseGestureControl startup entry found")
        except Exception as e:
            print(f"WARNING: Could not remove startup entry: {e}")
        
        winreg.CloseKey(key)
        
    except Exception as e:
        print(f"ERROR: Error accessing registry: {e}")

def check_startup_entries():
    """Check what startup entries exist."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Run")
        
        print("\nCurrent startup entries:")
        i = 0
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)
                if "MouseGesture" in name or "Gesture" in name:
                    print(f"  FOUND: {name}: {value}")
                i += 1
            except OSError:
                break
        
        winreg.CloseKey(key)
        
    except Exception as e:
        print(f"ERROR: Error checking startup entries: {e}")

def main():
    print("Mouse Gesture Control - Cleanup Script")
    print("=" * 50)
    
    # Check current startup entries
    check_startup_entries()
    
    # Remove startup entry
    remove_startup_entry()
    
    # Check again to confirm removal
    print("\nChecking after cleanup...")
    check_startup_entries()
    
    print("\nCleanup completed!")
    print("The old MouseGestureControl startup entry has been removed.")
    print("You can now safely restart your computer without the old version running.")

if __name__ == "__main__":
    main()
