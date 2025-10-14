
"""
GestureController
-----------------
Handles direction detection and swipe logic.
"""

import time
import math

class GestureController:
    def __init__(self, threshold=60, cooldown=0.5):
        self.start_x = None
        self.start_y = None
        self.active = False
        self.last_gesture_time = 0
        self.threshold = threshold
        self.cooldown = cooldown

    def start_gesture(self, x, y):
        self.start_x = x
        self.start_y = y
        self.active = True

    def detect_direction(self, x, y):
        if not self.active:
            return None

        now = time.time()
        # ⏳ Cooldown guard
        if now - self.last_gesture_time < self.cooldown:
            return None

        dx = x - self.start_x
        dy = y - self.start_y
        distance = math.hypot(dx, dy)

        if distance < self.threshold:
            return None

        # Determine main direction
        if abs(dx) > abs(dy):
            direction = "right" if dx > 0 else "left"
        else:
            direction = "down" if dy > 0 else "up"

        self.last_gesture_time = now
        return direction

    def end_gesture(self):
        self.active = False

