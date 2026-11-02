"""Test : diffusion XBee (broadcast) d'un ETAT_PLACES, comme le ferait Pi C.
Lancer depuis la racine du projet : python -m tests.xbee_broadcast_test
"""

import json
import time

import serial

from pi_b.config import XBEE_BAUDRATE, XBEE_PORT

INTERVALLE = 2  # secondes entre deux diffusions

print(f"Diffusion sur {XBEE_PORT} à {XBEE_BAUDRATE} bauds (Ctrl+C pour quitter)")

with serial.Serial(XBEE_PORT, XBEE_BAUDRATE, timeout=1) as ser:
    try:
        libre = True
        while True:
            message = json.dumps({"0": libre, "1": not libre})
            ser.write((message + "\n").encode())
            print(message)
            libre = not libre
            time.sleep(INTERVALLE)
    except KeyboardInterrupt:
        print("\nFin du test")
