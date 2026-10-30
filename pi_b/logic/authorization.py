from pi_b.logic.known_id import KnownCards


class Authorization:
    """Décide si une carte ouvre la barrière : carte connue ET au moins une place libre."""

    def __init__(self, known_cards: KnownCards) -> None:
        self.known_cards = known_cards
        self.free_spot = False

    def is_authorized(self, uid: int) -> bool:
        return self.known_cards.is_known(uid) and self.free_spot