
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
        if button == mouse.Button.left:
            self.left_pressed = pressed
        elif button == mouse.Button.right:
            self.right_pressed = pressed

        if self.left_pressed and self.right_pressed and pressed:
            self.on_both_press(x, y)
        elif not self.left_pressed or not self.right_pressed:
            self.on_release()

    def start(self):
        """Start listening for mouse input."""
        self.listener.start()
