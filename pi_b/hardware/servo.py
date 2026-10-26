from gpiozero import Servo

class Servo:
    """Low level hardware driver: It knows only angles (open/close)"""
    def __init__(self, pin: int, angle_min: float, angle_max: float = 180) -> None:

    def open_gate(self, angle: float) -> None:

    def close_gate(self, angle: float) -> None:

