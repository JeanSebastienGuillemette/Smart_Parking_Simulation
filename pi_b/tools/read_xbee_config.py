# Relit la configuration d'un module XBee.
# Lancer depuis la racine du projet : python -m tools.read_xbee_config
import argparse
import time

import serial

from help_queue import config


def send_at(ser, command: str, wait: float = 0.3) -> bytes:
    ser.write((command + "\r").encode())
    time.sleep(wait)
    return ser.read(ser.in_waiting or 1)


def read_config(port: str):
    ser = serial.Serial(port, 9600, timeout=2)
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
    parser = argparse.ArgumentParser(
        description="Lecture de la config XBee via mode commande AT"
    )
    parser.add_argument(
        "-p",
        "--port",
        default=config.PORT,
        required=config.PORT is None,
        help=(
            "Port série à interroger (ex: /dev/ttyUSB0, COM3). "
            "Par défaut: PORT dans .env"
        ),
    )
    args = parser.parse_args()

    command_mode, pan, my, dl, dh, ch = read_config(args.port)
    print(f"--- {args.port} ---")
    print("Mode commande :", command_mode)
    print("PAN ID :", pan)
    print("MY     :", my)
    print("DL     :", dl)
    print("DH     :", dh)
    print("Canal  :", ch)
