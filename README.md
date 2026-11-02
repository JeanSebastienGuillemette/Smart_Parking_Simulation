# Pi B — Cerveau et barrière

Module du **TP2 Stationnement intelligent**. Pi B est le serveur GATT de l'équipe : il décide si une carte est autorisée, contrôle la barrière (entrée et sortie) et relaie l'appel d'aide du client vers l'agent.

> **État :** en développement. La logique, la barrière, le lecteur RFID, le bouton d'aide, le BLE et le XBee fonctionnent.

## Matériel

| Composant | Usage |
|---|---|
| Lecteur RFID MFRC522 | Lecture des cartes à l'entrée |
| Servo SG90 | Barrière |
| Bouton d'aide | Appel d'aide du client |
| LED d'aide | Clignote pendant un appel d'aide |
| Buzzer passif | Bip court (aide), mélodie montante / descendante (carte autorisée / refusée) |
| XBee | Réception de `ETAT_PLACES` (broadcast de Pi C) |
| BLE | Serveur GATT pour Pi A et Pi C |

Câblage (BCM, modifiable dans `.env`) : servo 18, bouton 21, LED d'aide 20, buzzer 17.
MFRC522 sur SPI (broches fixes) : SDA 8, SCK 11, MOSI 10, MISO 9, RST 25.

## Fonctionnement

| Événement | Réaction |
|---|---|
| Carte lue | Décision → `RESULTAT_CARTE` vers Pi A ; si autorisée, bip long, ouverture puis fermeture après `GATE_CLOSING_DELAY` s |
| `ETAT_PLACES` reçu (XBee) | Mémorise le dernier état des places |
| `VOITURE_SORTIE` reçu (Pi A) | Bip long, ouvre la barrière |
| Appui sur le bouton d'aide | `APPEL_AIDE` vers Pi C, bip court, la LED d'aide clignote |
| `OUVERTURE_AGENT` reçu (Pi C) | Éteint la LED d'aide, bip long, ouvre la barrière |

**Règle d'autorisation :** carte dans la liste **ET** au moins une place libre dans le dernier `ETAT_PLACES`. Cette règle est isolée dans une seule méthode : `Authorization.is_authorized` (`logic/authorization.py`).

## Structure du projet

```
.
├── pi_b/
│   ├── __main__.py        Point d'entrée (python -m pi_b)
│   ├── app.py             Classe PiB : relie matériel, logique et BLE
│   ├── config.py          Lecture du .env et des chemins
│   ├── hardware/          Pilotes matériels
│   │   ├── rfid.py        MFRC522
│   │   ├── servo.py       SG90 (barrière)
│   │   ├── button.py      Bouton d'aide
│   │   ├── buzzer.py      Buzzer passif
│   │   └── xbee_receiver.py  Réception de ETAT_PLACES
│   ├── logic/             Logique (le matériel lui est passé en paramètre)
│   │   ├── authorization.py  Règle d'autorisation
│   │   ├── gate.py        Ouverture / fermeture automatique de la barrière
│   │   └── known_id.py    Liste des cartes autorisées
│   ├── transport/
│   │   └── gatt_server_ble.py  Serveur GATT (bluezero)
│   └── tools/             Configuration du module XBee
│       ├── configure_xbee.py
│       └── read_xbee_config.py
├── tests/                 Tests et simulations (mocks)
├── cards.example.json     Modèle de la liste des cartes
├── .env.example           Modèle de configuration
└── requirements.txt
```

`logic/` ne crée jamais de matériel ni de connexion : les objets lui sont passés en paramètre (`gate.py` importe `ServoMotor` seulement pour l'annotation de type). C'est ce qui permet de tester sans Pi A, sans Pi C et sans matériel.

## Installation

Sur le Raspberry Pi :

```bash
git clone <url-du-depot> pi_b
cd pi_b
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --no-deps mfrc522   # sans --no-deps, il installe RPi.GPIO, incompatible avec le Pi 5
```

## Configuration

1. Copier les modèles :
   ```bash
   cp .env.example .env
   cp cards.example.json cards.json
   ```
2. Ajouter les cartes autorisées dans `cards.json` : une liste d'objets `{"uid": <entier>, "name": "<texte>"}`.
   L'UID est l'entier affiché par `python -m tests.rfid_test`.
   La liste est toujours lue depuis `cards.json` à la racine du dépôt.
3. Ajuster `.env` au besoin (broches, délai de fermeture, paramètres XBee, UUIDs GATT).
4. Configurer le module XBee une fois (`PANID`, `MY`, `ID`, `CHANNEL` du `.env`) :
   ```bash
   python -m pi_b.tools.configure_xbee
   python -m pi_b.tools.read_xbee_config   # vérification
   ```

`.env` et `cards.json` sont ignorés par Git : ne jamais les committer.

## Lancement

```bash
python -m pi_b
```

## Tests et simulation

Pas de pytest : chaque test est un script, lancé depuis la racine avec `python -m tests.<nom>`.

| Script | Matériel requis | Vérifie |
|---|---|---|
| `authorization_test`, `known_id_test` | aucun | Règle d'autorisation, chargement de `cards.json` |
| `rfid_sensor_test` | aucun (faux lecteur) | `RFIDSensor` avec `KnownCards` |
| `rfid_test` | MFRC522 | Lecture des UID (pour remplir `cards.json`) |
| `servo_test` | servo | Ouverture / fermeture ; `calibrate` pour trouver les limites |
| `gate_test` | servo | Fermeture automatique de la barrière |
| `led_test` | LED | Allumer, éteindre, clignoter |
| `button_test` | bouton, LED | Chaque appui démarre / arrête le clignotement |
| `buzzer_test` | buzzer | Bip d'aide, mélodies de carte, choix de la fréquence |
| `buzzer_vader` | buzzer | Mélodie au buzzer |
| `ble_test` | tout + cellulaire (nRF Connect) | Caractéristiques GATT |
| `app_mock_test` | tout sauf Pi A / Pi C | Les 5 scénarios ci-dessous, au clavier |

Scénarios (`app_mock_test`) :

- `ETAT_PLACES` [libre, libre] + carte connue → autorisé, la barrière s'ouvre puis se ferme.
- Carte inconnue → refusé.
- `ETAT_PLACES` [occupée, occupée] + carte connue → refusé.
- `VOITURE_SORTIE` → la barrière s'ouvre.
- Bouton d'aide → `APPEL_AIDE` produit ; `OUVERTURE_AGENT` → la barrière s'ouvre.
