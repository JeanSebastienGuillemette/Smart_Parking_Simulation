"""Pi B"""
# python -m pi_b pour starter l'application
from gpiozero import LED

from pi_b.config import (
    BUZZER_PIN,
    GATE_ANGLE_CLOSED,
    GATE_ANGLE_OPEN,
    GATE_CLOSING_DELAY,
    HELP_BUTTON_PIN,
    HELP_LED_PIN,
    MELODY_ACCEPTED,
    MELODY_HELP,
    MELODY_REFUSED,
    SERVO_PIN,
    XBEE_BAUDRATE,
    XBEE_PORT,
)
from pi_b.hardware.button import PushButton
from pi_b.hardware.buzzer import PassiveBuzzer
from pi_b.hardware.rfid import RFIDSensor
from pi_b.hardware.servo import ServoMotor
from pi_b.hardware.xbee_receiver import XBeeReceiver
from pi_b.logic.authorization import Authorization
from pi_b.logic.gate import Gate
from pi_b.logic.known_id import KnownCards
from pi_b.transport.gatt_server_ble import BLEGattServer


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
        self.buzzer = PassiveBuzzer(BUZZER_PIN)
        self.help_led = LED(HELP_LED_PIN)
        self.ble = BLEGattServer(
            on_voiture_sortie=self.on_voiture_sortie,
            on_ouverture_agent=self.on_ouverture_agent,
        )

    def on_card(self, uid: int) -> None:
        if self.authorization.is_authorized(uid):
            print(f"RESULTAT_CARTE : autorisé ({uid})")
            self.buzzer.play(MELODY_ACCEPTED)
            self.ble.notify_resultat_carte(True)
            self.open_gate()
        else:
            print(f"RESULTAT_CARTE : refusé ({uid})")
            self.buzzer.play(MELODY_REFUSED)
            self.ble.notify_resultat_carte(False)

    def on_help(self) -> None:
        print("APPEL_AIDE")
        self.buzzer.play(MELODY_HELP)
        self.help_led.blink(on_time=0.5, off_time=0.5)
        self.ble.notify_appel_aide()

    def on_etat_places(self, places: dict[int, bool]) -> None:
        self.authorization.free_spot = any(places.values())
        print(f"ETAT_PLACES : {places}")

    def on_voiture_sortie(self) -> None:  # appelé par le BLE (Pi A)
        print("VOITURE_SORTIE : ouverture")
        self.open_gate()

    def on_ouverture_agent(self) -> None:  # appelé par le BLE (Pi C)
        print("OUVERTURE_AGENT : ouverture")
        self.help_led.off()
        self.open_gate()

    def open_gate(self) -> None:
        self.gate.open()


def run() -> None:
    pi_b = PiB()
    XBeeReceiver(XBEE_PORT, pi_b.on_etat_places, baud=XBEE_BAUDRATE).start()
    RFIDSensor(pi_b.on_card).start()

    print("Pi B prêt (Ctrl+C pour quitter)")
    pi_b.ble.publish()  # Ctrl+C pour quitter
    pi_b.gate.close()
    pi_b.help_led.off()
