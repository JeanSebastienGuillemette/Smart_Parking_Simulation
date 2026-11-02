from typing import Callable

import threading
import time

from mfrc522 import SimpleMFRC522

from pi_b.config import RFID_DEBOUNCE


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
