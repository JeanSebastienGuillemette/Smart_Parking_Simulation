"""Test : réception XBee (broadcast), affiche seulement le message reçu.
Lancer depuis la racine du projet : python -m tests.xbee_test
"""

import serial

from pi_b.config import XBEE_BAUDRATE, XBEE_PORT

print(f"Écoute sur {XBEE_PORT} à {XBEE_BAUDRATE} bauds (Ctrl+C pour quitter)")

with serial.Serial(XBEE_PORT, XBEE_BAUDRATE, timeout=1) as ser:
    try:
        while True:
            message = ser.readline().decode(errors="ignore").strip()
            if message:
                print(message)
    except KeyboardInterrupt:
        print("\nFin du test")
