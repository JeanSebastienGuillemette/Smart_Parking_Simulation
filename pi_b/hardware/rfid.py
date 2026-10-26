import logging
import threading
import time
from typing import Callable, Optional
 
from mfrc522 import SimpleMFRC522
 
logger = logging.getLogger(__name__)
 
 
class RFIDSensor:
    """Read RFID cards in a background thread and signal each new detection."""
 
    def __init__(
        self,
        on_card: Callable[[int], None],
        debounce_s: float = 3.0,
        poll_interval_s: float = 0.1,
    ) -> None:
        self.card_reader = SimpleMFRC522
        # TODO: create the SimpleMFRC522 instance
        # TODO: store on_card, debounce_s, poll_interval_s
        # TODO: debounce state -> what two things must you remember?
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
 
    def start(self) -> None:
        """Start the reading thread. Calling it twice must not create two threads."""
        # TODO: guard against double start
        # TODO: create the thread (target=self._run), daemon or not? why?
        ...
 
    def stop(self) -> None:
        """Ask the thread to stop, wait for it, release the GPIO."""
        # TODO: signal the event
        # TODO: join with a timeout
        # TODO: GPIO cleanup
        ...
 
    def read_card(self) -> Optional[int]:
        """One NON-blocking read attempt. Return the UID, or None if no card."""
        ...
 
    def _run(self) -> None:
        """Thread loop: runs until stop() is called."""
        # TODO: while the stop event is not set:
        #   - read_card()
        #   - if a uid and not a duplicate -> notify
        #   - wait poll_interval_s (hint: Event.wait() instead of time.sleep(), why?)
        ...
 
    def _is_duplicate(self, uid: int) -> bool:
        """True if same uid read less than debounce_s ago."""
        # TODO: use time.monotonic(), not time.time() -> why?
        ...
 
    def _notify(self, uid: int) -> None:
        """Deliver the uid to on_card. THIS is where the thread-safety decision lives."""
        # TODO: call on_card directly? or hand it to the main loop (GLib.idle_add)?
        # TODO: an exception in on_card must not kill the thread -> how?
        ...