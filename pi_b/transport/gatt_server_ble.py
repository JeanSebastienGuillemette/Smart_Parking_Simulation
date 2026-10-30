import os
from typing import Callable

from bluezero import peripheral

# périphérique
NOM_PERIPHERIQUE = os.environ["NOM_PERIPHERIQUE"]
PI_MAC_ADDRESS = os.environ["PI_MAC_ADDRESS"]

# UUID du service et des caractéristiques
SERVICE_GATE_UUID = os.environ["SERVICE_GATE_UUID"]
RESULTAT_CARTE_UUID = os.environ["RESULTAT_CARTE_UUID"]
VOITURE_SORTIE_UUID = os.environ["VOITURE_SORTIE_UUID"]
APPEL_AIDE_UUID = os.environ["APPEL_AIDE_UUID"]
OUVERTURE_AGENT_UUID = os.environ["OUVERTURE_AGENT_UUID"]

_SRV_ID = 1
_CHR_RESULTAT_CARTE = 1
_CHR_VOITURE_SORTIE = 2
_CHR_APPEL_AIDE = 3
_CHR_OUVERTURE_AGENT = 4


class BLEGattServer:
    def __init__(
        self,
        on_voiture_sortie: Callable[[], None],
        on_ouverture_agent: Callable[[], None],
    ) -> None:
        self._on_voiture_sortie = on_voiture_sortie
        self._on_ouverture_agent = on_ouverture_agent

        self._peripheral = peripheral.Peripheral(
            PI_MAC_ADDRESS, local_name=NOM_PERIPHERIQUE
        )
        self._peripheral.add_service(
            srv_id=_SRV_ID, uuid=SERVICE_GATE_UUID, primary=True
        )

        self._peripheral.add_characteristic(
            srv_id=_SRV_ID,
            chr_id=_CHR_RESULTAT_CARTE,
            uuid=RESULTAT_CARTE_UUID,
            value=[0],
            notifying=False,
            flags=["notify"],
        )
        self._resultat_carte_chr = self._peripheral.characteristics[-1]

        self._peripheral.add_characteristic(
            srv_id=_SRV_ID,
            chr_id=_CHR_VOITURE_SORTIE,
            uuid=VOITURE_SORTIE_UUID,
            value=[],
            notifying=False,
            flags=["write"],
            write_callback=self._on_voiture_sortie_write,
        )

        self._peripheral.add_characteristic(
            srv_id=_SRV_ID,
            chr_id=_CHR_APPEL_AIDE,
            uuid=APPEL_AIDE_UUID,
            value=[0],
            notifying=False,
            flags=["notify"],
        )
        self._appel_aide_chr = self._peripheral.characteristics[-1]

        self._peripheral.add_characteristic(
            srv_id=_SRV_ID,
            chr_id=_CHR_OUVERTURE_AGENT,
            uuid=OUVERTURE_AGENT_UUID,
            value=[],
            notifying=False,
            flags=["write"],
            write_callback=self._on_ouverture_agent_write,
        )

    def _on_voiture_sortie_write(self, value, options) -> None:
        self._on_voiture_sortie()

    def _on_ouverture_agent_write(self, value, options) -> None:
        self._on_ouverture_agent()

    def notify_resultat_carte(self, autorisee: bool) -> None:
        """Notifie Pi A du résultat de la décision d'autorisation."""
        self._resultat_carte_chr.set_value([1 if autorisee else 0])

    def notify_appel_aide(self) -> None:
        """Notifie Pi C qu'un appel d'aide a été déclenché."""
        self._appel_aide_chr.set_value([1])

    def publish(self) -> None:
        """Publie le périphérique et bloque en attente des connexions."""
        self._peripheral.publish()


def main() -> None:
    def on_voiture_sortie() -> None:
        print("TODO: ouvrir la barrière (voiture sortie)")

    def on_ouverture_agent() -> None:
        print("TODO: ouvrir la barrière (agent)")

    server = BLEGattServer(
        on_voiture_sortie=on_voiture_sortie,
        on_ouverture_agent=on_ouverture_agent,
    )
    server.publish()


if __name__ == "__main__":
    main()
