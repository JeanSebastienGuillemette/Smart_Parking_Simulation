from typing import Callable

import threading
import time

from mfrc522 import SimpleMFRC522

from pi_b.config import RFID_DEBOUNCE


class FakeReader:
    """Généré à 100% par Claude pour faire un faux reader rfid car les miens ne sont pas soudés!"""

    def __init__(self, uids: list[int]) -> None:
        self.uids = uids
        self.index = 0

    def read_id_no_block(self) -> int:
        time.sleep(5)
        uid = self.uids[self.index % len(self.uids)]
        self.index += 1
        return uid


class RFIDSensor:
    """Lis les cartes dans son propre thread et call on_card(uid)."""

    def __init__(self, on_card: Callable[[int], None], reader=None) -> None:
        self.reader = reader or SimpleMFRC522()
        self.on_card = on_card
        self.last_uid = None
        self.last_time = 0.0

    def start(self) -> None:
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        while True:
            uid = self.reader.read_id_no_block()
            now = time.monotonic()
            if uid is not None:
                if uid != self.last_uid or now - self.last_time > RFID_DEBOUNCE:
                    self.on_card(uid)
                self.last_uid = uid
                self.last_time = now
            time.sleep(0.1)
