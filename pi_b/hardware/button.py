from gpiozero import Button


class PushButton:
    def __init__(self, pin: int, on_press):
        self.button = Button(pin, bounce_time=0.05)
        self.button.when_pressed = on_press
