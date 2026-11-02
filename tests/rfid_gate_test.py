"""Test : lecture RFID réelle + autorisation (cards.json) + ouverture de la barrière.

Présenter une carte : si elle est dans cards.json, la barrière s'ouvre (et se referme
après GATE_CLOSING_DELAY). Pas de XBee ici : on considère qu'il reste toujours une place libre.

Lancer depuis la racine du projet : python -m tests.rfid_gate_test
"""

from time import sleep

from pi_b.config import (
    GATE_ANGLE_CLOSED,
    GATE_ANGLE_OPEN,
    GATE_CLOSING_DELAY,
    SERVO_PIN,
    BUZZER_PIN,
    MELODY_ACCEPTED,
    MELODY_REFUSED
)
from pi_b.hardware.rfid import RFIDSensor
from pi_b.hardware.servo import ServoMotor
from pi_b.hardware.buzzer import PassiveBuzzer
from pi_b.logic.authorization import Authorization
from pi_b.logic.gate import Gate
from pi_b.logic.known_id import KnownCards

cards = KnownCards()
auth = Authorization(cards)
auth.free_spot = True  # pas de XBee ici : on simule une place toujours libre

gate = Gate(
    ServoMotor(SERVO_PIN), GATE_ANGLE_OPEN, GATE_ANGLE_CLOSED, GATE_CLOSING_DELAY
)
buzzer = PassiveBuzzer(BUZZER_PIN)


def on_card(uid: int) -> None:
    if auth.is_authorized(uid):
        print(f"Carte {uid} : connue ({cards.name_of(uid)}) -> ouverture")
        buzzer.play(MELODY_ACCEPTED)
        gate.open()
    else:
        print(f"Carte {uid} : refusée")
        buzzer.play(MELODY_REFUSED)


RFIDSensor(on_card).start()

try:
    print("Présenter une carte (Ctrl+C pour quitter)")
    while True:
        sleep(1)
except KeyboardInterrupt:
    pass
gate.close()
print("Terminé")
