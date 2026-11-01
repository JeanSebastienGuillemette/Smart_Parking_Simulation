import threading

from gpiozero import PWMOutputDevice


class PassiveBuzzer:

    def __init__(self, pin: int, frequency: float = 2000) -> None:
        self.pwm = PWMOutputDevice(pin, frequency=frequency)
        self._timer: threading.Timer | None = None

    def beep(self, duration: float) -> None:
        if self._timer:
            self._timer.cancel()
        self.pwm.value = 0.5
        self._timer = threading.Timer(duration, self.pwm.off)
        self._timer.daemon = True
        self._timer.start()
