import dataclasses
import abc
from dailybkup.services import email_sender
import copy
from typing import Dict, Any
import dailybkup.dictutils as dictutils
import dailybkup.config.exceptions as config_exceptions
import dailybkup.services.email_sender as email_sender_mod


class INotifierConfig(abc.ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class EmailNotifierConfig(INotifierConfig):
    type_: str = "email"
    recipient_address: str
    sender_config: email_sender.IEmailSenderConfig


class NotificationConfigBuilder(dictutils.PDictBuilder[INotifierConfig]):
    def build(self, d: Dict[str, Any]) -> INotifierConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.pop("type_", "MISSING")
        if type_ == "email":
            return email_notification_config_builder.build(dict_)
        if type_ == "MISSING":
            raise config_exceptions.MissingConfigKey(
                "Missing key type_ for notification config"
            )
        raise ValueError(f'Invalid type_ "{type_}" for cleaner config')


class EmailNotificationConfigBuilder(dictutils.PDictBuilder[EmailNotifierConfig]):
    def build(self, d: Dict[str, Any]) -> EmailNotifierConfig:
        dict_ = copy.deepcopy(d)
        sender_config_raw = dict_.pop("sender_config")
        if sender_config_raw is None:
            raise config_exceptions.MissingConfigKey(
                "Missing key sender_config for email notification config"
            )
        sender_config = email_sender_mod.email_sender_config_builder.build(sender_config_raw)
        recipient_address = dict_.get("recipient_address")
        if recipient_address is None:
            raise config_exceptions.MissingConfigKey(
                "Missing key recipient_address for email notification config"
            )
        return EmailNotifierConfig(
            recipient_address=recipient_address, sender_config=sender_config
        )


email_notification_config_builder = EmailNotificationConfigBuilder()
notification_config_builder = NotificationConfigBuilder()
