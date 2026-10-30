"""Test : règle d'autorisation (carte connue ET place libre), sans matériel.

Lancer depuis la racine du projet : python -m tests.authorization_test
"""

from pi_b.logic.authorization import Authorization
from pi_b.logic.known_id import KnownCards

KNOWN_UID = 111111111111
UNKNOWN_UID = 999999999999


def check(description: str, result: bool) -> None:
    print(f"[{'OK' if result else 'ÉCHEC'}] {description}")


auth = Authorization(KnownCards())

check("avant le 1er broadcast XBee -> refusée", not auth.is_authorized(KNOWN_UID))

auth.free_spot = True  # simule le broadcast XBee : place libre
check("place libre + carte connue -> autorisée", auth.is_authorized(KNOWN_UID))
check("place libre + carte inconnue -> refusée", not auth.is_authorized(UNKNOWN_UID))

auth.free_spot = False  # simule le broadcast XBee : complet
check("complet + carte connue -> refusée", not auth.is_authorized(KNOWN_UID))