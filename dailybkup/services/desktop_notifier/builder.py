from .config import (
    IDesktopNotifierConfig,
    NotifySendNotifierConfig,
    MockDesktopNotifierConfig,
)
from .desktop_notifier import PDesktopNotifier, NotifySendNotifier, MockDesktopNotifier


class DesktopNotifierBuilder:
    def build(self, config: IDesktopNotifierConfig) -> PDesktopNotifier:
        if isinstance(config, NotifySendNotifierConfig):
            return NotifySendNotifier(command=config.command)
        if isinstance(config, MockDesktopNotifierConfig):
            return MockDesktopNotifier(directory=config.directory)
        raise ValueError(f"Unknown desktop notifier config: {config}")
