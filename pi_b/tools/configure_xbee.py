# Configure un module XBee avec les valeurs du .env.
# Lancer depuis la racine du projet : python -m tools.configure_xbee
import platform
import time
from types import SimpleNamespace

import serial
import serial.tools.list_ports

from help_queue import config


def list_available_ports():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("  Aucun port série détecté sur ce système.")
        return
    for p in ports:
        print(f"  {p.device} — {p.description}")


def example_port() -> str:
    return "COM3" if platform.system() == "Windows" else "/dev/ttyUSB0"


def send_at_command(ser, command: str) -> bytes:
    ser.write(command.encode() + b"\r")
    time.sleep(0.3)
    return ser.read(ser.in_waiting or 1)


def print_step(port: str, label: str, result: bytes):
    print(f"{port} - {label:<18}:", result)


def configure_module(args):
    try:
        ser = serial.Serial(args.port, 9600, timeout=1)
    except serial.SerialException as e:
        print(f"Impossible d'ouvrir {args.port} : {e}\n")
        print("Ports actuellement détectés :")
        list_available_ports()
        print(
            f"\nSur {platform.system()}, un port ressemble à : "
            f"{example_port()}"
        )
        return

    def step(label: str, command: str):
        print_step(args.port, label, send_at_command(ser, command))

    time.sleep(1.2)
    ser.write(b"+++")
    time.sleep(1.2)
    print_step(args.port, "Mode commande", ser.read(ser.in_waiting or 1))
    step("Reset usine", "ATRE")
    step("Sauvegarde", "ATWR")
    step("Firmware (VR)", "ATVR")
    step("AP -> 0", "ATAP0")
    step("PAN ID", "ATID" + args.panid)
    step("Canal", "ATCH" + args.channel)
    step("MY", "ATMY" + args.my)
    step("Dest DH", "ATDH0")
    step("Dest DL", "ATDLFFFF")
    step("NI", "ATNI" + args.id)
    # 802.15.4 n'a que 2 rôles : Coordinateur (CE1) ou End Device
    # (CE0, = "peer-to-peer").
    # Pas de "routeur" : ici tous les modules sont de simples End Device.
    step("CE (end device)", "ATCE0")

    if args.sleep:
        # SM=1 (Pin Sleep) n'a d'effet que si D8 est aussi mis en mode
        # "peripheral".
        step("D8 (SLEEP_RQ)", "ATD81")
        step("SM (pin sleep)", "ATSM1")
    else:
        step("SM (pas de veille)", "ATSM0")

    step("Sauvegarde", "ATWR")

    ser.close()
    sleep_mode = (
        "veille activée (pin sleep)" if args.sleep else "pas de veille"
    )
    print(
        f"\n{args.port} configuré "
        f"(MY={args.my}, PAN={args.panid}, {sleep_mode})"
    )


if __name__ == "__main__":
    config.require("PORT", "PANID", "MY", "ID")
    configure_module(
        SimpleNamespace(
            port=config.PORT,
            panid=config.PANID,
            my=config.MY,
            id=config.ID,
            channel=config.CHANNEL,
            sleep=config.SLEEP,
        )
    )
