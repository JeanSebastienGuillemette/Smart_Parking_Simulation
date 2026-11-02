"""Test : le buzzer passif (beep court, beep long, recherche de la meilleure fréquence).

Lancer depuis la racine du projet : python -m tests.buzzer_test
"""

from time import sleep

from pi_b.config import BEEP_LONG, BEEP_SHORT, BUZZER_PIN
from pi_b.hardware.buzzer import PassiveBuzzer

FREQUENCIES = [
    1000,
    2000,
    3000,
    4000,
]  # Hz, pour trouver celle où le buzzer est le plus fort

buzzer = PassiveBuzzer(BUZZER_PIN)

try:
    print(f"1. Beep court ({BEEP_SHORT} s) : bouton d'aide")
    buzzer.beep(BEEP_SHORT)
    sleep(BEEP_SHORT + 1)

    print(f"2. Beep long ({BEEP_LONG} s) : ouverture de la barrière")
    buzzer.beep(BEEP_LONG)
    sleep(BEEP_LONG + 1)

    print(
        "3. Beep long, puis beep court après 0.3 s : le son s'arrête à 0.5 s (le 2e remplace le 1er)"
    )
    buzzer.beep(BEEP_LONG)
    sleep(0.3)
    buzzer.beep(BEEP_SHORT)
    sleep(BEEP_LONG + 1)

    print("4. Fréquences : noter celle qui sonne le plus fort")
    for frequency in FREQUENCIES:
        print(f"   {frequency} Hz")
        buzzer.pwm.frequency = frequency
        buzzer.beep(0.5)
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    buzzer.pwm.off()
    buzzer.pwm.close()
    print("Terminé")
