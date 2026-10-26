from gpiozero import Button


class PushButton:
    def __init__(self, pin: str, on_press):
        self.button = Button(int(pin), bounce_time=0.05)
        self.button.when_pressed = on_press
