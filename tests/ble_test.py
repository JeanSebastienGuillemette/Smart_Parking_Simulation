"""Test : BLE avec un cellulaire (nRF Connect) ET le vrai matériel (barrière, LED, bouton).

Pas de faux lecteur RFID : les cartes sont simulées au clavier.
- Écrire dans VOITURE_SORTIE (...0002) -> la barrière s'ouvre puis se ferme.
- Écrire dans OUVERTURE_AGENT (...0004) -> la barrière s'ouvre, la LED d'aide s'éteint.
- S'abonner à APPEL_AIDE (...0003) puis appuyer sur le vrai bouton -> 01, la LED clignote.
- S'abonner à RESULTAT_CARTE (...0001) puis taper c / i ici -> 01 / 00, la barrière s'ouvre si 01.

Lancer depuis la racine du projet : python -m tests.ble_test
"""

import threading

from pi_b.app import PiB

KNOWN_UID = 111111111111
UNKNOWN_UID = 999999999999

pi_b = PiB()
pi_b.authorization.free_spot = True  # pas de XBee : on considère qu'il reste une place


def keyboard() -> None:
    while True:
        key = input().strip()
        if key == "c":
            pi_b.on_card(KNOWN_UID)
        elif key == "i":
            pi_b.on_card(UNKNOWN_UID)


threading.Thread(target=keyboard, daemon=True).start()
print(
    "Connecte-toi avec nRF Connect. c=carte connue  i=carte inconnue  (Ctrl+C pour quitter)"
)
pi_b.ble.publish()
pi_b.gate.close()
pi_b.help_led.off()
print("Terminé")
