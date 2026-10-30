"""Manual test: print the UID of each RFID card presented to the MFRC522.

Use it to check the wiring and to collect the UIDs of the authorized cards.

Run from the project root: python -m tests.rfid_test
"""

from time import sleep

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Present a card (Ctrl+C to quit)")
    while True:
        uid = reader.read_id()  # blocks until a card is detected
        print(f"Card UID: {uid}")
        sleep(1)  # avoid printing the same card many times
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    print("Done")