
"""
MouseGestureControl - Main Application Entry
--------------------------------------------
Runs the gesture control system, tying together:
- Gesture detection logic
- Mouse input listener
- Action triggers
"""

import json
from gesture_controller import GestureController
from input_listener import InputListener
from actions import perform_action

def load_config(path="config.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Error] Could not load config file: {e}")
        return {}

def main():
    print("🎧 Mouse Gesture Control - Starting...")
    config = load_config()
    debug_enabled = config.get("debug", False)
    threshold = config.get("threshold", 60)
    cooldown = config.get("cooldown", 0.5)
    use_alt = config.get("use_alt_instead_of_ctrl", False)

    gesture = GestureController(threshold=threshold, cooldown=cooldown)

    def on_both_press(x, y):
        gesture.start_gesture(x, y)

    def on_move(x, y):
        direction = gesture.detect_direction(x, y)
        if direction:
            action = config.get(direction)
            if action:
                perform_action(
                    action,
                    debug=debug_enabled,
                    direction=direction,
                    use_alt=use_alt
                )
            gesture.end_gesture()

    def on_release():
        gesture.end_gesture()

    listener = InputListener(on_both_press, on_move, on_release)
    listener.start()

    print(f"✅ Gesture control active. Debug mode: {debug_enabled}")
    print(f"   Threshold: {threshold}px | Cooldown: {cooldown}s | ALT-for-CTRL: {use_alt}")
    print("Hold both mouse buttons and swipe. Press Ctrl+C to exit.\n")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully...")

if __name__ == "__main__":
    main()

