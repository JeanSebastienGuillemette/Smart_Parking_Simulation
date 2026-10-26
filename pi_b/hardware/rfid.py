from typing import Callable, Optional
from mfrc522 import SimpleMFRC522

class RFIDSensor:
    """Read RFID cards and signal each new detections"""

    def __init__(self, on_card: Callable[[int], None], debounce_timer_ms: float = 3.0) -> None:

    def read_card(self) -> Optional[int]:

    def start(self) -> None:

    def stop(self) -> None:

    def _is_double(self, uidL int) -> Bool: