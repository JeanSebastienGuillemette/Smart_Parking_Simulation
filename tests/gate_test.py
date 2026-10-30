"""Test : la barrière (Gate + ServoMotor) avec la fermeture automatique.

Lancer depuis la racine du projet : python -m tests.gate_test
"""

from time import sleep

from pi_b.config import GATE_ANGLE_CLOSED, GATE_ANGLE_OPEN, SERVO_PIN
from pi_b.hardware.servo import ServoMotor
from pi_b.logic.gate import Gate

CLOSING_DELAY = 3  # court pour le test (le vrai délai vient de GATE_CLOSING_DELAY)

servo = ServoMotor(SERVO_PIN)
gate = Gate(servo, GATE_ANGLE_OPEN, GATE_ANGLE_CLOSED, CLOSING_DELAY)

try:
    print(f"1. Ouverture, fermeture automatique après {CLOSING_DELAY} s")
    gate.open()
    print(f"   ouverte : {gate.is_opened}")
    sleep(CLOSING_DELAY + 1)
    print(f"   ouverte : {gate.is_opened} (attendu : False)")

    print("2. Ouverture, puis 2e ouverture après 2 s : le délai repart à zéro")
    gate.open()
    sleep(2)
    gate.open()
    sleep(2)
    print(f"   2 s après la 2e ouverture, ouverte : {gate.is_opened} (attendu : True)")
    sleep(CLOSING_DELAY)
    print(f"   ouverte : {gate.is_opened} (attendu : False)")

    print("3. Ouverture puis fermeture manuelle")
    gate.open()
    sleep(1)
    gate.close()
    print(f"   ouverte : {gate.is_opened} (attendu : False)")
except KeyboardInterrupt:
    pass
finally:
    gate.close()
    servo.close()
    print("Terminé")