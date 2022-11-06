from typing import Dict
from .config import IEmailSenderConfig, MockEmailSenderConfig, MailGunEmailSenderConfig
from .email_sender import PEmailSender, MockEmailSender, MailGunEmailSender


class EmailSenderBuilder:
    def build(
        self,
        config: IEmailSenderConfig,
        environ: Dict[str, str],
    ) -> PEmailSender:
        if isinstance(config, MockEmailSenderConfig):
            return MockEmailSender(directory=config.directory)
        if isinstance(config, MailGunEmailSenderConfig):
            api_key = environ["DAILYBKUP_MAILGUN_API_KEY"]
            return MailGunEmailSender(
                base_url=config.base_url,
                from_=config.from_,
                api_key=api_key,
            )
        raise ValueError(f"Unknown email sender config: {config}")
