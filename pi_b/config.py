import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")

# Gate
SERVO_PIN = int(os.getenv("SERVO_PIN", "18"))
GATE_CLOSING_DELAY = float(os.getenv("GATE_CLOSING_DELAY", "10"))
GATE_ANGLE_OPEN = 90
GATE_ANGLE_CLOSED = 0

# RFID
RFID_DEBOUNCE = float(os.getenv("RFID_DEBOUNCE", "3"))

# Help button
HELP_BUTTON_PIN = int(os.getenv("HELP_BUTTON_PIN", "21"))
HELP_LED_PIN = int(os.getenv("AGENT_LED", "20"))

# Buzzer
BUZZER_PIN = int(os.getenv("BUZZER_PIN", "17"))
BEEP_LONG = 1.2
BEEP_SHORT = 0.2

# XBee
XBEE_PORT = os.getenv("PORT", "/dev/ttyUSB0")
XBEE_BAUDRATE = int(os.getenv("BAUDRATE", "9600"))
XBEE_PANID = os.getenv("PANID", "")
XBEE_MY = os.getenv("MY", "")
XBEE_ID = os.getenv("ID", "")
XBEE_CHANNEL = os.getenv("CHANNEL", "")
XBEE_SLEEP = os.getenv("SLEEP") == "1"

# BLE (GATT server)
BLE_DEVICE_NAME = os.getenv("NOM_PERIPHERIQUE", "Pi-B")
SERVICE_GATE_UUID = os.getenv("SERVICE_GATE_UUID", "")
RESULTAT_CARTE_UUID = os.getenv("RESULTAT_CARTE_UUID", "")
VOITURE_SORTIE_UUID = os.getenv("VOITURE_SORTIE_UUID", "")
APPEL_AIDE_UUID = os.getenv("APPEL_AIDE_UUID", "")
OUVERTURE_AGENT_UUID = os.getenv("OUVERTURE_AGENT_UUID", "")
