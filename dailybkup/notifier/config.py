import dataclasses
import abc
from dailybkup.services import email_sender
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


desktop_notifier_config_builder: configmod.PConfigBuilder[DesktopNotifierConfig]
desktop_notifier_config_builder = configmod.GenericBuilder(
    DesktopNotifierConfig,
    configmod.bs.SubBuilder(
        "sender_config",
        desktop_notifier.desktop_notifier_config_builder,
    ),
)

email_notification_config_builder: configmod.PConfigBuilder[EmailNotifierConfig]
email_notification_config_builder = configmod.GenericBuilder(
    EmailNotifierConfig,
    configmod.bs.SubBuilder(
        "sender_config", email_sender_mod.email_sender_config_builder
    ),
    configmod.bs.Required("recipient_address"),
)

notification_config_builder: configmod.TypeDispatcherConfigBuilder[NotifierConfig]
notification_config_builder = configmod.TypeDispatcherConfigBuilder(
    {
        "email": email_notification_config_builder,
        "desktop": desktop_notifier_config_builder,
    }
)
