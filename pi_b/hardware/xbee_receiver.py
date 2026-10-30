import serial

from pi_b import config


class XBeeReceiver:
    def __init__(self, port: str, baud: int = 9600, timeout: float = 1):
        self.port = port
        self.ser = serial.Serial(port, baud, timeout=timeout)

    def receive(self) -> str:
        return self.ser.readline().decode(errors="ignore").strip()

    def listen_loop(self):
        print("En écoute...")
        while True:
            data = self.receive()
            if data:
                print("Reçu :", data)

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    XBeeReceiver(config.XBEE_PORT, config.XBEE_BAUDRATE).listen_loop()