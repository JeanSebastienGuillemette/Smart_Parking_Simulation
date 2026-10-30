"""Pi B"""

from signal import pause

from pi_b.config import (
    GATE_ANGLE_CLOSED,
    GATE_ANGLE_OPEN,
    GATE_CLOSING_DELAY,
    HELP_BUTTON_PIN,
    SERVO_PIN,
)
from pi_b.hardware.button import PushButton
from pi_b.hardware.rfid import FakeReader, RFIDSensor
from pi_b.hardware.servo import ServoMotor
from pi_b.logic.authorization import Authorization
from pi_b.logic.gate import Gate
from pi_b.logic.known_id import KnownCards

MOCK_UIDS = [111111111111, 999999999999]


def run() -> None:
    authorization = Authorization(KnownCards())
    authorization.free_spot = (
        True  # TODO: updaté par le broadcast XBee (ETAT_PLACES), si un spot free mettre à True, sinon False
    )
    gate = Gate(
        ServoMotor(SERVO_PIN), GATE_ANGLE_OPEN, GATE_ANGLE_CLOSED, GATE_CLOSING_DELAY
    )

    def on_card(uid: int) -> None:
        if authorization.is_authorized(uid):
            print(f"RESULTAT_CARTE : autorisé ({uid})")  # TODO: envoyer à Pi A (BLE)
            gate.open()
        else:
            print(f"RESULTAT_CARTE : refusé ({uid})")  # TODO: envoyer à Pi A (BLE)

    def on_help() -> None:
        print("APPEL_AIDE")  # TODO: envoyer à Pi C (BLE)

    RFIDSensor(on_card, reader=FakeReader(MOCK_UIDS)).start()
    button = PushButton(HELP_BUTTON_PIN, on_help)

    print("Pi B prêt (Ctrl+C pour quitter)")
    try:
        pause()  # attend les événements (cartes ou bouton)
    except KeyboardInterrupt:
        gate.close()
