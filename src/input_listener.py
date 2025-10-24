
"""
InputListener
-------------
Listens for global mouse events using pynput.
Detects when both left and right buttons are pressed.
"""

from pynput import mouse


class InputListener:
    def __init__(self, on_both_press, on_move, on_release):
        self.left_pressed = False
        self.right_pressed = False
        self.listener = mouse.Listener(
            on_click=self._on_click, on_move=on_move)
        self.on_both_press = on_both_press
        self.on_release = on_release

    def _on_click(self, x, y, button, pressed):
        # Store previous state to detect simultaneous clicks
        prev_left = self.left_pressed
        prev_right = self.right_pressed
        
        # Update button states
        if button == mouse.Button.left:
            self.left_pressed = pressed
        elif button == mouse.Button.right:
            self.right_pressed = pressed

        # Handle button press events
        if pressed:
            # Check if both buttons are being pressed within a short time
            if (button == mouse.Button.left and prev_right) or \
               (button == mouse.Button.right and prev_left):
                self.on_both_press(x, y)
                return True  # Consume the event
        
        # Handle button release
        if not pressed and (not self.left_pressed or not self.right_pressed):
            self.on_release()
            
        return True  # Always consume the event to prevent system actions

    def start(self):
        """Start listening for mouse input."""
        self.listener.start()
