"""Test : le buzzer passif (mélodies, remplacement, recherche de la meilleure fréquence).

Lancer depuis la racine du projet : python -m tests.buzzer_test
"""

from time import sleep

from pi_b.config import BUZZER_PIN, MELODY_ACCEPTED, MELODY_HELP, MELODY_REFUSED
from pi_b.hardware.buzzer import PassiveBuzzer

FREQUENCIES = [
    1000,
    2000,
    3000,
    4000,
]  # Hz, pour trouver celle où le buzzer est le plus fort

buzzer = PassiveBuzzer(BUZZER_PIN)

try:
    print("1. Bip court : bouton d'aide")
    buzzer.play(MELODY_HELP)
    sleep(1)

    print("2. Mélodie montante : carte autorisée")
    buzzer.play(MELODY_ACCEPTED)
    sleep(1.5)

    print("3. Mélodie descendante : carte refusée")
    buzzer.play(MELODY_REFUSED)
    sleep(1.5)

    print(
        "4. Note de 1.2 s, puis bip court après 0.3 s : le son s'arrête à 0.5 s (le 2e remplace le 1er)"
    )
    buzzer.play([(2000, 1.2)])
    sleep(0.3)
    buzzer.play(MELODY_HELP)
    sleep(2)

    print("5. Fréquences : noter celle qui sonne le plus fort")
    for frequency in FREQUENCIES:
        print(f"   {frequency} Hz")
        buzzer.play([(frequency, 0.5)])
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    buzzer.pwm.off()
    buzzer.pwm.close()
    print("Terminé")
