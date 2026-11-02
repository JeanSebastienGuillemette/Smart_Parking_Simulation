"""Manual test: turn an LED on, off, then blink it.

Run from the project root: python -m tests.led_test
"""

import os
from time import sleep

from dotenv import load_dotenv
from gpiozero import LED

ON_TIME = 2  # seconds the LED stays on
BLINK_COUNT = 5
BLINK_TIME = 0.3  # seconds on, then seconds off

load_dotenv()
led = LED(int(os.getenv("HELP_LED_PIN", "20")))

try:
    print("LED on")
    led.on()
    sleep(ON_TIME)

    print("LED off")
    led.off()
    sleep(1)

    print(f"Blinking {BLINK_COUNT} times")
    led.blink(on_time=BLINK_TIME, off_time=BLINK_TIME, n=BLINK_COUNT, background=False)
except KeyboardInterrupt:
    pass
finally:
    led.off()
    led.close()
    print("Done")
