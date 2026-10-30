# Pi B — Cerveau et barrière

Module du **TP2 Stationnement intelligent**. Pi B est le serveur GATT de l'équipe : il décide si une carte est autorisée, contrôle la barrière (entrée et sortie) et relaie l'appel d'aide du client vers l'agent.

> **État :** en développement. La structure du projet est en place, la logique reste à écrire.

## Matériel

| Composant | Usage |
|---|---|
| Lecteur RFID MFRC522 | Lecture des cartes à l'entrée |
| Servo SG90 | Barrière |
| Bouton d'aide | Appel d'aide du client |
| XBee | Réception de `ETAT_PLACES` (broadcast de Pi C) |
| BLE | Serveur GATT pour Pi A et Pi C |

Câblage (broches GPIO) : **À décider**.

## Fonctionnement

| Événement | Réaction |
|---|---|
| Carte lue | Décision → `RESULTAT_CARTE` vers Pi A ; si autorisée, ouverture puis fermeture après X s |
| `ETAT_PLACES` reçu (XBee) | Mémorise le dernier état des places |
| `VOITURE_SORTIE` reçu (Pi A) | Ouvre la barrière |
| Appui sur le bouton d'aide | `APPEL_AIDE` vers Pi C |
| `OUVERTURE_AGENT` reçu (Pi C) | Ouvre la barrière |

**Règle d'autorisation :** carte dans la liste **ET** au moins une place libre dans le dernier `ETAT_PLACES`. Cette règle est isolée dans une seule méthode de `logic/gate.py`

## Structure du projet

```
.
├── pi_b/
│   ├── __main__.py        Point d'entrée (python -m pi_b)
│   ├── config.py          Lecture du .env et des chemins
│   ├── hardware/          Pilotes matériels
│   │   ├── rfid.py        MFRC522
│   │   ├── servo.py       SG90 (barrière)
│   │   └── button.py      Bouton d'aide
│   ├── logic/             Logique, sans dépendance matérielle
│   │   ├── gate.py        Autorisation et contrôle de la barrière
│   │   └── known_id.py    Liste des cartes autorisées
│   └── transport/         Communication
│       ├── ble.py         Serveur GATT
│       └── xbee.py        Réception de ETAT_PLACES
├── tests/                 Tests et simulations (mocks)
├── cards.example.json     Modèle de la liste des cartes
├── .env.example           Modèle de configuration
└── requirements.txt
```

`logic/` ne doit jamais importer `hardware/` ni `transport/` directement : les dépendances lui sont passées. C'est ce qui permet de tester sans Pi A, sans Pi C et sans matériel.

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
3. Ajuster `.env` au besoin.

`.env` et `cards.json` sont ignorés par Git : ne jamais les committer.

## Lancement

```bash
python -m pi_b
```

## Tests et simulation

Scénarios à couvrir sans Pi A ni Pi C (mocks dans `tests/`) :

- `ETAT_PLACES` [libre, libre] + carte connue → autorisé, la barrière s'ouvre puis se ferme.
- Carte inconnue → refusé.
- `ETAT_PLACES` [occupée, occupée] + carte connue → refusé.
- `VOITURE_SORTIE` → la barrière s'ouvre.
- Bouton d'aide → `APPEL_AIDE` produit ; `OUVERTURE_AGENT` → la barrière s'ouvre.

Commande de lancement des tests : **À décider** (par ex. `python -m pytest`).
