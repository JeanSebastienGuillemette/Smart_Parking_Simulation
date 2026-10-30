from time import sleep

from pi_b.hardware.rfid import FakeReader, RFIDSensor
from pi_b.logic.known_id import KnownCards

MOCK_UIDS = [
    111111111111,
    222222222222,
    333333333333,
    999999999999,
]

cards = KnownCards()


def on_card(uid: int) -> None:
    if cards.is_known(uid):
        print(f"Carte {uid} : connue ({cards.name_of(uid)})")
    else:
        print(f"Carte {uid} : inconnue")


print("Une carte toutes les 5 s (Ctrl+C pour quitter)")
RFIDSensor(on_card, reader=FakeReader(MOCK_UIDS)).start()

try:
    sleep(len(MOCK_UIDS) * 5 + 1)
except KeyboardInterrupt:
    pass
print("Terminé")