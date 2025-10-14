
"""
Actions
-------
Defines system actions triggered by gestures.
"""

from pynput import keyboard
import time

kb = keyboard.Controller()

def show_debug_message(direction, action):
    print(f"[Gesture] Swipe {direction.upper()} → {action.replace('_', ' ').title()}")
    time.sleep(0.05)

def perform_action(action, debug=False, direction=None, use_alt=False):
    if debug and direction:
        show_debug_message(direction, action)

    # Choose modifier key based on config
    modifier_key = keyboard.Key.alt if use_alt else keyboard.Key.ctrl

    if action == "task_view":
        with kb.pressed(keyboard.Key.cmd):
            kb.press(keyboard.Key.tab)
            kb.release(keyboard.Key.tab)

    elif action == "close_task_view":
        kb.press(keyboard.Key.esc)
        kb.release(keyboard.Key.esc)

    elif action == "desktop_left":
        with kb.pressed(keyboard.Key.cmd):
            with kb.pressed(modifier_key):
                kb.press(keyboard.Key.left)
                kb.release(keyboard.Key.left)

    elif action == "desktop_right":
        with kb.pressed(keyboard.Key.cmd):
            with kb.pressed(modifier_key):
                kb.press(keyboard.Key.right)
                kb.release(keyboard.Key.right)
