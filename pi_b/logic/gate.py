import threading

from pi_b.hardware.servo import ServoMotor


class Gate:
    """Simulation d'une barrière gérée par un servo. open() l'ouvre et la referme après le délai prévu."""

    def __init__(
        self,
        servo: ServoMotor,
        angle_open: float,
        angle_closed: float,
        closing_delay: float,
    ) -> None:
        self.servo = servo
        self.angle_open = angle_open
        self.angle_closed = angle_closed
        self.closing_delay = closing_delay
        self._is_opened = False
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()
        self.close()

    def open(self) -> None:
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self.servo.move_to(self.angle_open)
            self._is_opened = True
            self._timer = threading.Timer(self.closing_delay, self.close)
            self._timer.daemon = True
            self._timer.start()

    def close(self) -> None:
        with self._lock:
            self.servo.move_to(self.angle_closed)
            self._is_opened = False

    @property
    def is_opened(self) -> bool:
        return self._is_opened
