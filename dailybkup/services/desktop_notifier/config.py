import copy
from typing import Dict, Any
import abc
import dataclasses
import dailybkup.dictutils as dictutils
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


notify_send_notifier_config_builder = dictutils.DictBuilder(
    [],
    ["type_", "command"],
    NotifySendNotifierConfig,
    missing_key_exception=configmod.MissingConfigKey,
    unknown_key_exception=configmod.UnkownConfigKey,
)
mock_notifier_config_builder = dictutils.DictBuilder(
    ["directory"],
    ["type_"],
    MockDesktopNotifierConfig,
    missing_key_exception=configmod.MissingConfigKey,
    unknown_key_exception=configmod.UnkownConfigKey,
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
