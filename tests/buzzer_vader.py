"""Test : la marche impériale (ouverture) au buzzer passif.

Lancer depuis la racine du projet : python -m tests.buzzer_vader
"""

from time import sleep

from pi_b.config import BUZZER_PIN
from pi_b.hardware.buzzer import PassiveBuzzer

# Fréquences des notes (Hz)
G4, GB4, EB4, BB4 = 392, 370, 311, 466
D5, EB5 = 587, 622

QUARTER = 0.5  # s, une noire à 120 bpm
NOTE_RATIO = (
    0.9  # la note sonne 90 % de sa durée : petit silence entre deux notes identiques
)

# (fréquence, durée en s)
MELODY = [
    (G4, QUARTER),
    (G4, QUARTER),
    (G4, QUARTER),
    (EB4, 0.35),
    (BB4, 0.15),
    (G4, QUARTER),
    (EB4, 0.35),
    (BB4, 0.15),
    (G4, 2 * QUARTER),
    (D5, QUARTER),
    (D5, QUARTER),
    (D5, QUARTER),
    (EB5, 0.35),
    (BB4, 0.15),
    (GB4, QUARTER),
    (EB4, 0.35),
    (BB4, 0.15),
    (G4, 2 * QUARTER),
]

buzzer = PassiveBuzzer(BUZZER_PIN)

try:
    print("Marche impériale")
    for frequency, duration in MELODY:
        buzzer.play([(frequency, duration * NOTE_RATIO)])
        sleep(duration)
except KeyboardInterrupt:
    pass
finally:
    buzzer.pwm.off()
    buzzer.pwm.close()
    print("Terminé")
