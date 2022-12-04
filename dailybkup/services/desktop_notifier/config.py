import copy
from typing import Dict, Any
import abc
import dataclasses
import dailybkup.dictutils as dictutils
import dailybkup.config.exceptions as config_exceptions


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


class DesktopNotifierConfigBuilder(dictutils.PDictBuilder[IDesktopNotifierConfig]):
    def build(self, d: Dict[str, Any]) -> IDesktopNotifierConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.get("type_", "MISSING")
        if type_ == "notify-send":
            return notify_send_notifier_config_builder.build(dict_)
        if type_ == "mock":
            return mock_notifier_config_builder.build(dict_)
        if type_ == "MISSING":
            raise config_exceptions.MissingConfigKey(
                "Missing key type_ for desktop notifier config"
            )
        raise ValueError(f'Invalid type_ "{type_}" for email sender config')


notify_send_notifier_config_builder = dictutils.DictBuilder(
    [],
    ["type_", "command"],
    NotifySendNotifierConfig,
    missing_key_exception=config_exceptions.MissingConfigKey,
    unknown_key_exception=config_exceptions.UnkownConfigKey,
)
desktop_notifier_config_builder = DesktopNotifierConfigBuilder()
mock_notifier_config_builder = dictutils.DictBuilder(
    ["directory"],
    ["type_"],
    MockDesktopNotifierConfig,
    missing_key_exception=config_exceptions.MissingConfigKey,
    unknown_key_exception=config_exceptions.UnkownConfigKey,
)
