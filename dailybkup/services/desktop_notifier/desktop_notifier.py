from typing import Protocol
from .petition import DesktopNotificationPetition


class PDesktopNotifier(Protocol):
    def send(self, petition: DesktopNotificationPetition) -> None:
        ...


class NotifySendNotifier:
    def __init__(self, command: str):
        self._command = command

    def send(self, petition: DesktopNotificationPetition) -> None:
        raise NotImplementedError()
