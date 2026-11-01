"""Pi B"""

from gpiozero import LED

from pi_b.config import (
    GATE_ANGLE_CLOSED,
    GATE_ANGLE_OPEN,
    GATE_CLOSING_DELAY,
    HELP_BUTTON_PIN,
    HELP_LED_PIN,
    SERVO_PIN,
    XBEE_BAUDRATE,
    XBEE_PORT,
)
from pi_b.hardware.button import PushButton
from pi_b.hardware.rfid import FakeReader, RFIDSensor
from pi_b.hardware.servo import ServoMotor
from pi_b.hardware.xbee_receiver import XBeeReceiver
from pi_b.logic.authorization import Authorization
from pi_b.logic.gate import Gate
from pi_b.logic.known_id import KnownCards
from pi_b.transport.gatt_server_ble import BLEGattServer

MOCK_UIDS = [111111111111, 999999999999]


class PiB:
    """Pi B : relie la décision, la barrière et le bouton d'aide."""

    def __init__(self) -> None:
        self.authorization = Authorization(KnownCards())
        self.gate = Gate(
            ServoMotor(SERVO_PIN),
            GATE_ANGLE_OPEN,
            GATE_ANGLE_CLOSED,
            GATE_CLOSING_DELAY,
        )
        self.button = PushButton(HELP_BUTTON_PIN, self.on_help)
        self.help_led = LED(HELP_LED_PIN)
        self.ble = BLEGattServer(
            on_voiture_sortie=self.on_voiture_sortie,
            on_ouverture_agent=self.on_ouverture_agent,
        )

    def on_card(self, uid: int) -> None:
        if self.authorization.is_authorized(uid):
            print(f"RESULTAT_CARTE : autorisé ({uid})")
            self.ble.notify_resultat_carte(True)
            self.gate.open()
        else:
            print(f"RESULTAT_CARTE : refusé ({uid})")
            self.ble.notify_resultat_carte(False)

    def on_help(self) -> None:
        print("APPEL_AIDE")
        self.help_led.blink(on_time=0.5, off_time=0.5)  # signal visuel pour le client
        self.ble.notify_appel_aide()

    def on_etat_places(
        self, places: dict[int, bool]
    ) -> None:
        self.authorization.free_spot = any(places.values())
        print(f"ETAT_PLACES : {places}")

    def on_voiture_sortie(self) -> None:  # appelé par le BLE (Pi A)
        print("VOITURE_SORTIE : ouverture")
        self.gate.open()

    def on_ouverture_agent(self) -> None:  # appelé par le BLE (Pi C)
        print("OUVERTURE_AGENT : ouverture")
        self.help_led.off()  # l'agent a répondu à l'appel
        self.gate.open()


def run() -> None:
    pi_b = PiB()
    XBeeReceiver(XBEE_PORT, pi_b.on_etat_places, baud=XBEE_BAUDRATE).start()
    RFIDSensor(pi_b.on_card, reader=FakeReader(MOCK_UIDS)).start()  # TODO: vrai lecteur

    print("Pi B prêt (Ctrl+C pour quitter)")
    pi_b.ble.publish()  # annonce le BLE et attend (Ctrl+C l'arrête)
    pi_b.gate.close()
    pi_b.help_led.off()
