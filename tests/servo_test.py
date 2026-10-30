"""Manual test: the SG90 servo simulates the gate (0° = closed, 90° = open).

Port of the ESP32 ServoMotor class (ledc duty values) to gpiozero PWM.

Run from the project root:
    python -m tests.servo_test              # open/close the gate a few times
    python -m tests.servo_test calibrate    # type duty values to find the real limits
"""

import os
import sys
from time import sleep

from dotenv import load_dotenv
from gpiozero import PWMOutputDevice

# Same meaning as the ESP32 ledcSetup() values: copy them from ServoMotor.h
FREQUENCY = 50  # Hz -> 20 ms period
RESOLUTION = 16  # bits -> duty from 0 to 65535
MIN_DUTY = 1638  # duty at 0°   (1638 / 65536 * 20 ms ≈ 0.5 ms)
MAX_DUTY = 8192  # duty at 180° (8192 / 65536 * 20 ms ≈ 2.5 ms)

ANGLE_CLOSED = 0
ANGLE_OPEN = 90
CYCLES = 3
DELAY = 2  # seconds between moves
MOVE_TIME = 0.5  # seconds of pulses to reach the angle before releasing

MAX_DUTY_VALUE = 2**RESOLUTION


class ServoMotor:
    def __init__(self, pin: int, min_duty: int, max_duty: int) -> None:
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.pwm = PWMOutputDevice(pin, frequency=FREQUENCY)

    def write_duty(self, duty: int) -> None:
        self.pwm.value = duty / MAX_DUTY_VALUE

    def move_to(self, angle: int) -> None:
        duty = self.angle_to_duty(angle)
        self.write_duty(duty)
        print(f"angle: {angle} duty: {duty}")
        # Software PWM makes the servo jitter while holding: stop the pulses once
        # it has reached the angle, the gears keep the gate in place.
        sleep(MOVE_TIME)
        self.pwm.off()

    def angle_to_duty(self, angle: int) -> int:
        angle = min(max(angle, 0), 180)
        return self.min_duty + (angle * (self.max_duty - self.min_duty)) // 180

    def close(self) -> None:
        self.pwm.close()


def calibrate(servo: ServoMotor) -> None:
    """Send raw duty values to find where the servo actually stops."""
    print(f"Type a duty value (0-{MAX_DUTY_VALUE - 1}), empty line to quit.")
    print("Note the values where the horn stops moving (or starts buzzing).")
    while text := input("duty> ").strip():
        duty = int(text)
        servo.write_duty(duty)
        print(f"duty: {duty} pulse: {duty / MAX_DUTY_VALUE * 1000 / FREQUENCY:.2f} ms")


load_dotenv()
servo = ServoMotor(int(os.getenv("SERVO_PIN", "18")), MIN_DUTY, MAX_DUTY)

try:
    if len(sys.argv) > 1 and sys.argv[1] == "calibrate":
        calibrate(servo)
    else:
        for i in range(CYCLES):
            print(f"[{i + 1}/{CYCLES}] Opening gate")
            servo.move_to(ANGLE_OPEN)
            sleep(DELAY)
            print(f"[{i + 1}/{CYCLES}] Closing gate")
            servo.move_to(ANGLE_CLOSED)
            sleep(DELAY)
except KeyboardInterrupt:
    pass
finally:
    servo.move_to(ANGLE_CLOSED)
    servo.close()
    print("Done")