import uuid
from typing import Protocol, Optional
import os
import glob
import dataclasses
import json


@dataclasses.dataclass(frozen=True, kw_only=True)
class EmailPetition:
    recipient_address: str
    subject: str
    body: str


class PEmailSender(Protocol):
    def send(self, email_petition: EmailPetition) -> None:
        ...


class MockEmailSender(PEmailSender):
    def __init__(
        self,
        directory: str,
    ):
        self._directory = directory
        self._last_email_petition = None
        self._count = 0
        self._last_filename: Optional[str] = None

    @property
    def count(self):
        return len(os.listdir(self._directory))

    @property
    def last_email_petition(self):
        list_of_files = glob.glob(f"{self._directory}/*")
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file) as f:
            return EmailPetition(**json.load(f))

    def send(self, email_petition: EmailPetition) -> None:
        filename = str(uuid.uuid1())
        self._last_filename = filename
        with open(f"{self._directory}/{filename}", "w") as f:
            json.dump(dataclasses.asdict(email_petition), f)
