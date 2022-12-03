from . import config as configmod
from . import builder as sut
from .desktop_notifier import NotifySendNotifier


class TestDesktopNotifierBuilder:
    def test_builds_notify_send_notifier(self):
        config = configmod.NotifySendNotifierConfig()
        environ = {}
        builder = sut.DesktopNotifierBuilder()
        service = builder.build(config, environ)
        assert isinstance(service, NotifySendNotifier)
