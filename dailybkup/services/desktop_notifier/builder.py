from .config import (
    IDesktopNotifierConfig,
    NotifySendNotifierConfig,
    MockDesktopNotifierConfig,
)
from .desktop_notifier import PDesktopNotifier, NotifySendNotifier, MockDesktopNotifier
from typing import Dict


class DesktopNotifierBuilder:
    def build(
        self, config: IDesktopNotifierConfig, environ: Dict[str, str]
    ) -> PDesktopNotifier:
        if isinstance(config, NotifySendNotifierConfig):
            return NotifySendNotifier(command=config.command)
        if isinstance(config, MockDesktopNotifierConfig):
            return MockDesktopNotifier(directory=config.directory)
        raise ValueError(f"Unknown desktop notifier config: {config}")
