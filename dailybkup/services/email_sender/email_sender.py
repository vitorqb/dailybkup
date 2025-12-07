import uuid
from typing import Protocol, Optional
import os
import glob
import dataclasses
import json
import requests


@dataclasses.dataclass(frozen=True, kw_only=True)
class EmailPetition:
    recipient_address: str
    subject: str
    body: str


class PEmailSender(Protocol):
    def send(self, email_petition: EmailPetition) -> None: ...


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


class MailGunEmailSender(PEmailSender):
    def __init__(
        self,
        *,
        base_url: str,
        from_: str,
        api_key: str,
    ):
        self._base_url = base_url
        self._from = from_
        self._session = requests.Session()
        self._session.auth = ("api", api_key)

    def send(self, email_petition: EmailPetition) -> None:
        self._session.post(
            f"{self._base_url}/messages",
            data={
                "from": self._from,
                "to": email_petition.recipient_address,
                "subject": email_petition.subject,
                "text": email_petition.body,
            },
        ).raise_for_status()
