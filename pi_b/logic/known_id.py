import json

from pi_b.config import ROOT_DIR

CARDS_PATH = ROOT_DIR / "cards.json"


class KnownCards:
    """Liste de cartes authorisées, chargées du fichier cards.json: [{"uid": int, "name": str}, ...]"""

    def __init__(self) -> None:
        self.card_list: dict[int, str] = {}
        self.load()

    def load(self) -> None:
        try:
            with open(CARDS_PATH, encoding="utf-8") as cards_json_file:
                cards = json.load(cards_json_file)
            self.card_list = {int(card["uid"]): card["name"] for card in cards}
        except (OSError, ValueError, KeyError, TypeError) as error:
            print(f"Chargement échoué {CARDS_PATH}, toutes les cartes vont être refusées: {error}")
            self.card_list = {}

    def is_known(self, uid: int) -> bool:
        return uid in self.card_list

    def name_of(self, uid: int) -> str | None:
        return self.card_list.get(uid)
