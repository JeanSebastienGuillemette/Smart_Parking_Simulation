import time

import serial

from pi_b import config


def send_at(ser, command: str, wait: float = 0.3) -> bytes:
    ser.write((command + "\r").encode())
    time.sleep(wait)
    return ser.read(ser.in_waiting or 1)


def read_config():
    ser = serial.Serial(config.XBEE_PORT, config.XBEE_BAUDRATE, timeout=2)
    time.sleep(1.2)
    ser.write(b"+++")
    time.sleep(1.2)
    command_mode = ser.read(10)
    pan = send_at(ser, "ATID")
    my = send_at(ser, "ATMY")
    dl = send_at(ser, "ATDL")
    dh = send_at(ser, "ATDH")
    ch = send_at(ser, "ATCH")
    ser.close()
    return command_mode, pan, my, dl, dh, ch


if __name__ == "__main__":
    command_mode, pan, my, dl, dh, ch = read_config()
    print(f"--- {config.XBEE_PORT} ---")
    print("Mode commande :", command_mode)
    print("PAN ID :", pan)
    print("MY     :", my)
    print("DL     :", dl)
    print("DH     :", dh)
    print("Canal  :", ch)
