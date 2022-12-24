import abc
import dataclasses
import dailybkup.config as configmod


class IDesktopNotifierConfig(abc.ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class NotifySendNotifierConfig(IDesktopNotifierConfig):
    type_: str = "notify-send"
    command: str = "notify-send"


@dataclasses.dataclass(frozen=True, kw_only=True)
class MockDesktopNotifierConfig(IDesktopNotifierConfig):
    type_: str = "mock"
    directory: str


notify_send_notifier_config_builder = configmod.GenericBuilder(
    NotifySendNotifierConfig,
    configmod.bs.Optional("type_", "notify-send"),
    configmod.bs.Optional("command", "notify-send"),
)
mock_notifier_config_builder = configmod.GenericBuilder(
    MockDesktopNotifierConfig,
    configmod.bs.Required("directory"),
    configmod.bs.Optional("type_", "mock"),
)
desktop_notifier_config_builder: configmod.TypeDispatcherConfigBuilder[
    IDesktopNotifierConfig
]
desktop_notifier_config_builder = configmod.TypeDispatcherConfigBuilder(
    {
        "notify-send": notify_send_notifier_config_builder,
        "mock": mock_notifier_config_builder,
    }
)
