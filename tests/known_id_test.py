"""Test : liste des cartes autorisées (KnownCards), sans lecteur RFID.

Lancer depuis la racine du projet : python -m tests.known_id_test
"""

import tempfile
from pathlib import Path

import pi_b.logic.known_id as known_id
from pi_b.logic.known_id import KnownCards

MOCK_UIDS = [111111111111, 222222222222, 333333333333]
UNKNOWN_UID = 999999999999


def load_from(content: str | None) -> KnownCards:
    """Charge KnownCards depuis un fichier temporaire (None = fichier absent)."""
    original_path = known_id.CARDS_PATH
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "cards.json"
        if content is not None:
            path.write_text(content, encoding="utf-8")
        known_id.CARDS_PATH = path
        try:
            return KnownCards()
        finally:
            known_id.CARDS_PATH = original_path


def check(description: str, result: bool) -> None:
    print(f"[{'OK' if result else 'ÉCHEC'}] {description}")


# Le vrai cards.json avec les UIDs de test
cards = KnownCards()
for uid in MOCK_UIDS:
    check(f"carte connue {uid} ({cards.name_of(uid)})", cards.is_known(uid))
check("carte inconnue refusée", not cards.is_known(UNKNOWN_UID))
check("nom d'une carte inconnue = None", cards.name_of(UNKNOWN_UID) is None)

# Fichiers problématiques : toutes les cartes doivent être refusées
check("fichier absent -> refusée", not load_from(None).is_known(MOCK_UIDS[0]))
check("JSON invalide -> refusée", not load_from('[{"uid":, }]').is_known(MOCK_UIDS[0]))
check(
    "clé uid manquante -> refusée",
    not load_from('[{"name": "A"}]').is_known(MOCK_UIDS[0]),
)
check(
    "uid pas un nombre -> refusée",
    not load_from('[{"uid": "abc", "name": "A"}]').is_known(MOCK_UIDS[0]),
)