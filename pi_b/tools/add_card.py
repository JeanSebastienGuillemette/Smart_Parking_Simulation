import json

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from pi_b.logic.known_id import CARDS_PATH


def load_cards() -> list[dict]:
    try:
        with open(CARDS_PATH, encoding="utf-8") as cards_file:
            return json.load(cards_file)
    except (OSError, ValueError):
        return []


def save_cards(cards: list[dict]) -> None:
    with open(CARDS_PATH, "w", encoding="utf-8") as cards_file:
        json.dump(cards, cards_file, indent=4, ensure_ascii=False)
        cards_file.write("\n")


def add_card() -> None:
    cards = load_cards()
    reader = SimpleMFRC522()
    try:
        print(f"Cartes chargées depuis {CARDS_PATH} ({len(cards)})")
        print("Présenter une carte (Ctrl+C pour quitter)")
        while True:
            uid = reader.read_id()
            existing = next((card for card in cards if int(card["uid"]) == uid), None)
            if existing:
                print(f"Carte déjà connue : {uid} ({existing['name']})")
                name = input(
                    f"Nouveau nom (vide pour garder « {existing['name']} ») : "
                ).strip()
                if name:
                    existing["name"] = name
                    save_cards(cards)
                    print("Mis à jour.")
            else:
                name = input(
                    f"Carte {uid}, nom à enregistrer (vide pour ignorer) : "
                ).strip()
                if name:
                    cards.append({"uid": uid, "name": name})
                    save_cards(cards)
                    print("Ajoutée.")
                else:
                    print("Ignorée.")
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        print("\nTerminé.")


if __name__ == "__main__":
    add_card()
