import dataclasses
import abc
import dailybkup.dictutils as dictutils
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


mock_email_sender_config_builder = dictutils.DictBuilder(
    ["directory"],
    ["type_"],
    MockEmailSenderConfig,
    missing_key_exception=configmod.MissingConfigKey,
    unknown_key_exception=configmod.UnkownConfigKey,
)
mailgun_email_sender_config_builder = dictutils.DictBuilder(
    ["base_url", "from_"],
    ["type_"],
    MailGunEmailSenderConfig,
    missing_key_exception=configmod.MissingConfigKey,
    unknown_key_exception=configmod.UnkownConfigKey,
)
email_sender_config_builder: configmod.TypeDispatcherConfigBuilder[IEmailSenderConfig]
email_sender_config_builder = configmod.TypeDispatcherConfigBuilder(
    {
        "mock": mock_email_sender_config_builder,
        "mailgun": mailgun_email_sender_config_builder,
    }
)
