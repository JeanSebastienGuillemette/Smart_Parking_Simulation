import serial


class XBeeTransmitter:
    def __init__(self, port: str, baud: int = 9600, timeout: float = 1):
        self.port = port
        self.ser = serial.Serial(port, baud, timeout=timeout)

    def send(self, message: str):
        self.ser.write(message.encode())

    def receive(self, timeout: float = 2) -> str:
        self.ser.timeout = timeout
        return self.ser.readline().decode(errors="ignore").strip()

    def close(self):
        self.ser.close()
