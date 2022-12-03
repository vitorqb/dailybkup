from .config import IDesktopNotifierConfig, NotifySendNotifierConfig
from .desktop_notifier import PDesktopNotifier, NotifySendNotifier
from typing import Dict


class DesktopNotifierBuilder:
    def build(
        self, config: IDesktopNotifierConfig, environ: Dict[str, str]
    ) -> PDesktopNotifier:
        if isinstance(config, NotifySendNotifierConfig):
            return NotifySendNotifier(command=config.command)
        raise ValueError(f"Unknown desktop notifier config: {config}")
