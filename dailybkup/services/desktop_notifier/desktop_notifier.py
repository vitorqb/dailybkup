import dataclasses
import json
import glob
import os
import uuid
from typing import Protocol
from .petition import DesktopNotificationPetition
import dailybkup.osutils as osutils


class PDesktopNotifier(Protocol):
    def send(self, petition: DesktopNotificationPetition) -> None:
        ...


class NotifySendNotifier:
    def __init__(
        self,
        command: str,
    ):
        self._command = command

    def send(self, petition: DesktopNotificationPetition) -> None:
        osutils.run([self._command, petition.summary, petition.body])


class MockDesktopNotifier:
    def __init__(self, directory: str):
        self._directory = directory

    def send(self, petition: DesktopNotificationPetition) -> None:
        filename = str(uuid.uuid1())
        with open(f"{self._directory}/{filename}", "w") as f:
            json.dump(dataclasses.asdict(petition), f)

    @property
    def count(self) -> int:
        return len(os.listdir(self._directory))

    @property
    def last_petition(self):
        list_of_files = glob.glob(f"{self._directory}/*")
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file) as f:
            return DesktopNotificationPetition(**json.load(f))
