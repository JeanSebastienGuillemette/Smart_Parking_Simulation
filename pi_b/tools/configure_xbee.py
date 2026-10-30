import time

import serial

from pi_b import config


def send_at(ser: serial.Serial, command: str) -> bytes:
    ser.write(command.encode() + b"\r")
    time.sleep(0.3)
    return ser.read(ser.in_waiting or 1)


def configure() -> None:
    panid = config.XBEE_PANID
    my = config.XBEE_MY
    node_id = config.XBEE_ID
    channel = config.XBEE_CHANNEL
    sleep = config.XBEE_SLEEP
    if not (panid and my and node_id and channel):
        print("Remplir PANID, MY, ID et CHANNEL dans .env")
        return

    ser = serial.Serial(config.XBEE_PORT, config.XBEE_BAUDRATE, timeout=1)
    time.sleep(1.2)
    ser.write(b"+++")  # entre en mode commande AT
    time.sleep(1.2)
    print("Mode commande :", ser.read(ser.in_waiting or 1))

    commands = [
        "ATRE",
        "ATAP0",
        f"ATID{panid}",
        f"ATCH{channel}",
        f"ATMY{my}",
        "ATDH0",
        "ATDLFFFF",
        f"ATNI{node_id}",
        "ATCE0",
    ]
    commands += ["ATD81", "ATSM1"] if sleep else ["ATSM0"]
    commands.append("ATWR")

    for command in commands:
        print(f"{command:<10}:", send_at(ser, command))
    ser.close()
    print(f"\n{config.XBEE_PORT} configuré (MY={my}, PAN={panid}, veille={sleep})")


if __name__ == "__main__":
    configure()
