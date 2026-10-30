"""Simulation des 5 scénarios de pi_b.md au clavier, sans Pi A ni Pi C.

Lancer depuis la racine du projet : python -m tests.app_mock_test
"""

from pi_b.app import PiB

KNOWN_UID = 111111111111
UNKNOWN_UID = 999999999999

pi_b = PiB()

print(
    "c=carte connue  i=carte inconnue  l=places libres  p=complet  "
    "s=sortie  a=agent  q=quitter  (bouton d'aide : le vrai bouton)"
)
try:
    while (key := input("> ").strip()) != "q":
        if key == "c":
            pi_b.on_card(KNOWN_UID)
        elif key == "i":
            pi_b.on_card(UNKNOWN_UID)
        elif key == "l":
            pi_b.on_etat_places({1: True, 2: True})
        elif key == "p":
            pi_b.on_etat_places({1: False, 2: False})
        elif key == "s":
            pi_b.on_voiture_sortie()
        elif key == "a":
            pi_b.on_ouverture_agent()
except KeyboardInterrupt:
    pass
pi_b.gate.close()
print("Terminé")