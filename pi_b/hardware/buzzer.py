import threading

from gpiozero import PWMOutputDevice


class PassiveBuzzer:

    def __init__(self, pin: int) -> None:
        self.pwm = PWMOutputDevice(pin)
        self._stop = threading.Event()

    def play(self, notes) -> None:
        self._stop.set()
        self._stop = threading.Event()
        threading.Thread(
            target=self._play, args=(notes, self._stop), daemon=True
        ).start()

    def _play(self, notes, stop: threading.Event) -> None:
        for frequency, duration in notes:
            self.pwm.frequency = frequency
            self.pwm.value = 0.5
            if stop.wait(duration):
                return
        self.pwm.off()
