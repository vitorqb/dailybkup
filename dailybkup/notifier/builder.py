import dailybkup.services.email_sender as email_sender_mod
from .config import INotifierConfig, EmailNotifierConfig
from .notifier import INotifier, EmailNotifier


class NotifierBuilder:
    def __init__(self, email_sender_builder: email_sender_mod.EmailSenderBuilder):
        self._email_sender_builder = email_sender_builder

    def build(self, config: INotifierConfig) -> INotifier:
        if isinstance(config, EmailNotifierConfig):
            email_sender = self._email_sender_builder.build(config.sender_config)
            email_notifier = EmailNotifier(
                sender=email_sender,
                recipient_address=config.recipient_address,
            )
            return email_notifier
        raise ValueError(f"Unknown notifier config: {config}")
