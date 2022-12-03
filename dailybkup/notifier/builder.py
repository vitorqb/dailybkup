import dailybkup.services.email_sender as email_sender_mod
import dailybkup.services.desktop_notifier as desktop_notifier_mod
from .config import NotifierConfig, EmailNotifierConfig, DesktopNotifierConfig
from .notifier import Notifier, EmailNotifier, DesktopNotifier
from typing import Dict


class NotifierBuilder:
    def __init__(
        self,
        email_sender_builder: email_sender_mod.EmailSenderBuilder,
        desktop_notifier_builder: desktop_notifier_mod.DesktopNotifierBuilder,
    ):
        self._email_sender_builder = email_sender_builder
        self._desktop_notifier_builder = desktop_notifier_builder

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
        if isinstance(config, DesktopNotifierConfig):
            sender = self._desktop_notifier_builder.build(config.sender_config, environ)
            notifier = DesktopNotifier(sender=sender)
            return notifier
        raise ValueError(f"Unknown notifier config: {config}")
