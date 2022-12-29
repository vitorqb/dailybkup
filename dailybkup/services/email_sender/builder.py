from typing import Dict
from .config import IEmailSenderConfig, MockEmailSenderConfig, MailGunEmailSenderConfig
from .email_sender import PEmailSender, MockEmailSender, MailGunEmailSender


class EmailSenderBuilder:
    def build(
        self,
        config: IEmailSenderConfig,
    ) -> PEmailSender:
        if isinstance(config, MockEmailSenderConfig):
            return MockEmailSender(directory=config.directory)
        if isinstance(config, MailGunEmailSenderConfig):
            return MailGunEmailSender(
                base_url=config.base_url,
                from_=config.from_,
                api_key=config.api_key,
            )
        raise ValueError(f"Unknown email sender config: {config}")
