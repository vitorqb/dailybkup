import dataclasses
import abc
import copy
from typing import Dict, Any
import dailybkup.dictutils as dictutils
import dailybkup.config.exceptions as config_exceptions


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


class EmailSenderConfigBuilder(dictutils.PDictBuilder[IEmailSenderConfig]):
    def build(self, d: Dict[str, Any]) -> IEmailSenderConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.get("type_", "MISSING")
        if type_ == "mock":
            return mock_email_sender_config_builder.build(dict_)
        if type_ == "mailgun":
            return mailgun_email_sender_config_builder.build(dict_)
        if type_ == "MISSING":
            raise config_exceptions.MissingConfigKey(
                "Missing key type_ for email sender config"
            )
        raise ValueError(f'Invalid type_ "{type_}" for email sender config')


mock_email_sender_config_builder = dictutils.DictBuilder(
    ["directory"],
    ["type_"],
    MockEmailSenderConfig,
    missing_key_exception=config_exceptions.MissingConfigKey,
    unknown_key_exception=config_exceptions.UnkownConfigKey,
)
mailgun_email_sender_config_builder = dictutils.DictBuilder(
    ["base_url", "from_"],
    ["type_"],
    MailGunEmailSenderConfig,
    missing_key_exception=config_exceptions.MissingConfigKey,
    unknown_key_exception=config_exceptions.UnkownConfigKey,
)
email_sender_config_builder = EmailSenderConfigBuilder()
