import ast
import threading
from typing import Callable

import serial

from pi_b import config


class XBeeReceiver:
    """Classe pour recevoir les messages XBee via le port série"""

    def __init__(
        self,
        port: str,
        on_etat_places: Callable[[dict[int, bool]], None],
        baud: int = 9600,
        timeout: float = 1,
    ):
        self.port = port
        self.on_etat_places = on_etat_places
        self.ser = serial.Serial(port, baud, timeout=timeout)

    def start(self) -> None:
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def receive(self) -> str:
        return self.ser.readline().decode(errors="ignore").strip()

    def listen_loop(self):
        print("En écoute...")
        while True:
            data = self.receive()
            if data:
                try:
                    self.on_etat_places(
                        ast.literal_eval(data)
                    )  # ex. "{1: True, 2: False}"
                except (ValueError, SyntaxError, AttributeError, TypeError) as e:
                    print(f"XBee : message ignoré : {data!r}: {e}")

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    XBeeReceiver(config.XBEE_PORT, print, config.XBEE_BAUDRATE).listen_loop()
