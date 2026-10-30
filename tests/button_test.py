"""Manual test: each button press toggles the LED blinking on/off.

Run from the project root: python -m tests.button_test
"""

import os
from signal import pause

from dotenv import load_dotenv
from gpiozero import LED, Button

BLINK_TIME = 0.3  # seconds on, then seconds off

load_dotenv()
led = LED(int(os.getenv("AGENT_LED", "20")))
button = Button(int(os.getenv("HELP_BUTTON_PIN", "21")), bounce_time=0.05)

blinking = False


def toggle_blink() -> None:
    global blinking
    blinking = not blinking
    if blinking:
        print("Button pressed: blinking")
        led.blink(on_time=BLINK_TIME, off_time=BLINK_TIME)
    else:
        print("Button pressed: stopped")
        led.off()


button.when_pressed = toggle_blink

try:
    print("Press the button to start/stop blinking (Ctrl+C to quit)")
    pause()
except KeyboardInterrupt:
    pass
finally:
    led.off()
    led.close()
    button.close()
    print("Done")