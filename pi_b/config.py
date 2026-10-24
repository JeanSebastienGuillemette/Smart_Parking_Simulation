import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")

CARDS_FILE = Path(os.getenv("CARDS_FILE", ROOT_DIR / "cards.json"))
