from typing import Protocol
from .petition import DesktopNotificationPetition


class PDesktopNotifier(Protocol):
    def send(self, petition: DesktopNotificationPetition) -> None:
        ...
