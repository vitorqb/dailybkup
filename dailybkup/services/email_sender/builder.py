from .config import IEmailSenderConfig, MockEmailSenderConfig
from .email_sender import PEmailSender, MockEmailSender


class EmailSenderBuilder:
    def build(self, config: IEmailSenderConfig) -> PEmailSender:
        if isinstance(config, MockEmailSenderConfig):
            return MockEmailSender(directory=config.directory)
        raise ValueError(f"Unknown email sender config: {config}")
