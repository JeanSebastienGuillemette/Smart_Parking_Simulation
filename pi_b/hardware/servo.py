from time import sleep

from gpiozero import PWMOutputDevice

FREQUENCY = 50
RESOLUTION = 16
MIN_DUTY = 1638
MAX_DUTY = 8192
MOVE_TIME = 0.5


class ServoMotor:

    def __init__(self, pin: int) -> None:
        self.pwm = PWMOutputDevice(pin, frequency=FREQUENCY)

    def move_to(self, angle: float) -> None:
        self.pwm.value = self.angle_to_duty(angle) / 2**RESOLUTION
        sleep(MOVE_TIME)
        self.pwm.off()

    @staticmethod
    def angle_to_duty(angle: float) -> int:
        angle = min(max(angle, 0), 180)
        return int(MIN_DUTY + angle * (MAX_DUTY - MIN_DUTY) / 180)

    def close(self) -> None:
        self.pwm.close()
