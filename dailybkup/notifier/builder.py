import dailybkup.services.email_sender as email_sender_mod
from .config import NotifierConfig, EmailNotifierConfig
from .notifier import Notifier, EmailNotifier
from typing import Dict


class NotifierBuilder:
    def __init__(self, email_sender_builder: email_sender_mod.EmailSenderBuilder):
        self._email_sender_builder = email_sender_builder

    def build(self, config: NotifierConfig, environ: Dict[str, str]) -> Notifier:
        if isinstance(config, EmailNotifierConfig):
            email_sender = self._email_sender_builder.build(
                config.sender_config, environ
            )
            email_notifier = EmailNotifier(
                sender=email_sender,
                recipient_address=config.recipient_address,
            )
            return email_notifier
        raise ValueError(f"Unknown notifier config: {config}")
