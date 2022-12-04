import dataclasses
import abc
from dailybkup.services import email_sender
import copy
from typing import Dict, Any
import dailybkup.dictutils as dictutils
import dailybkup.config as configmod
import dailybkup.services.email_sender as email_sender_mod
import dailybkup.services.desktop_notifier as desktop_notifier


class NotifierConfig(abc.ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class EmailNotifierConfig(NotifierConfig):
    type_: str = "email"
    recipient_address: str
    sender_config: email_sender.IEmailSenderConfig


@dataclasses.dataclass(frozen=True, kw_only=True)
class DesktopNotifierConfig(NotifierConfig):
    type_: str = "desktop"
    sender_config: desktop_notifier.IDesktopNotifierConfig


class EmailNotificationConfigBuilder(dictutils.PDictBuilder[EmailNotifierConfig]):
    def build(self, d: Dict[str, Any]) -> EmailNotifierConfig:
        dict_ = copy.deepcopy(d)
        sender_config_raw = dict_.pop("sender_config")
        if sender_config_raw is None:
            raise configmod.MissingConfigKey(
                "Missing key sender_config for email notification config"
            )
        sender_config = email_sender_mod.email_sender_config_builder.build(
            sender_config_raw
        )
        recipient_address = dict_.get("recipient_address")
        if recipient_address is None:
            raise configmod.MissingConfigKey(
                "Missing key recipient_address for email notification config"
            )
        return EmailNotifierConfig(
            recipient_address=recipient_address, sender_config=sender_config
        )


class DesktopNotifierConfigBuilder(dictutils.PDictBuilder[DesktopNotifierConfig]):
    def build(self, d: Dict[str, Any]) -> DesktopNotifierConfig:
        dict_ = copy.deepcopy(d)
        sender_config_raw = dict_.pop("sender_config")
        if sender_config_raw is None:
            raise configmod.MissingConfigKey(
                "Missing key sender_config for desktop notification config"
            )
        sender_config = desktop_notifier.desktop_notifier_config_builder.build(
            sender_config_raw
        )
        return DesktopNotifierConfig(sender_config=sender_config)


desktop_notifier_config_builder = DesktopNotifierConfigBuilder()
email_notification_config_builder = EmailNotificationConfigBuilder()
notification_config_builder: configmod.TypeDispatcherConfigBuilder[NotifierConfig]
notification_config_builder = configmod.TypeDispatcherConfigBuilder(
    {
        "email": email_notification_config_builder,
        "desktop": desktop_notifier_config_builder,
    }
)
