import dataclasses
import abc
import dailybkup.config as configmod


class IEmailSenderConfig(abc.ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class MockEmailSenderConfig(IEmailSenderConfig):
    type_: str = "mock"
    directory: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class MailGunEmailSenderConfig(IEmailSenderConfig):
    type_: str = "mailgun"
    base_url: str
    from_: str
    api_key: str


mock_email_sender_config_builder = configmod.GenericBuilder(
    MockEmailSenderConfig,
    configmod.bs.Required("directory"),
    configmod.bs.Optional("type_", "mock"),
)
mailgun_email_sender_config_builder = configmod.GenericBuilder(
    MailGunEmailSenderConfig,
    configmod.bs.Required("base_url", "from_"),
    configmod.bs.Optional("type_", "mailgun"),
    configmod.bs.Optional(
        "api_key", configmod.default.env("DAILYBKUP_MAILGUN_API_KEY")
    ),
)
email_sender_config_builder: configmod.TypeDispatcherConfigBuilder[IEmailSenderConfig]
email_sender_config_builder = configmod.TypeDispatcherConfigBuilder(
    {
        "mock": mock_email_sender_config_builder,
        "mailgun": mailgun_email_sender_config_builder,
    }
)
