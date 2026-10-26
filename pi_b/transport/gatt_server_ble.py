# sur votre Raspberry Pi
# serveur GATT avec bluezero

import os

from dotenv import load_dotenv

from bluezero import async_tools
from bluezero import peripheral

load_dotenv()

# clés pour la communication
NOM_PERIPHERIQUE = os.environ["NOM_PERIPHERIQUE"]
SERVICE_GATE_UUID = os.environ["SERVICE_TEMPERATURE_UUID"]
CARD_READ_UUID = os.environ["CARACTERISTIQUE_UUID"]
OPEN_GATE_REQUEST_UUID = os.environ["COMMANDE_UUID"]
PI_MAC_ADDRESS = os.environ["PI_MAC_ADDRESS"]

# signature d'un abonnement ou désabonnement.
# notifying à True indique un abonnement.
# Ici, on automatise les notifications vers le client (timer)
def enregistrement_notifications(notifying, characteristic):
    def notifier():
        characteristic.set_value((f"{temp:.1f}".encode()))
        return characteristic.is_notifying

    if notifying:
        async_tools.add_timer_seconds(5, notifier)


# signature d'une réception de données (flag write)
# le client envoie un nombre signé (ex: "+2", "-3") qui est ajouté à temp
# def get_request(value, options):


def main():
    # initialisation du service
    pi_ble = peripheral.Peripheral(PI_MAC_ADDRESS, local_name=NOM_PERIPHERIQUE)
    pi_ble.add_service(srv_id=1, uuid=SERVICE_GATE_UUID, primary=True)

    pi_ble.add_characteristic(
        srv_id=1,
        chr_id=1,
        uuid=CARD_READ_UUID,
        value=[],
        notifying=False,
        flags=["read", "notify"],
        read_callback=get_request,
        notify_callback=enregistrement_notifications,
    )

    pi_ble.add_characteristic(
        srv_id=1,
        chr_id=2,
        uuid=OPEN_GATE_REQUEST_UUID,
        value=[],
        notifying=False,
        flags=["write"],
        write_callback=recevoir_commande,
    )

    # attente des connexions
    print("Serveur GATT configuré, tentative de publication...")
    pi_ble.publish()


if __name__ == "__main__":
    main()
