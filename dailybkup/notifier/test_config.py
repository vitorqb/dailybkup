import dailybkup.notifier.config as sut
import dailybkup.services.email_sender as email_sender
import dailybkup.services.desktop_notifier as desktop_notifier


class TestNotificationConfigBuilder:
    def test_build_email(self):
        d = {
            "type_": "email",
            "recipient_address": "foo@bar.baz",
            "sender_config": {"type_": "mock", "directory": "./foo"},
        }
        config = sut.notification_config_builder.build(d)
        assert config == sut.EmailNotifierConfig(
            recipient_address="foo@bar.baz",
            sender_config=email_sender.MockEmailSenderConfig(directory="./foo"),
        )

    def test_build_desktop(self):
        d = {"type_": "desktop", "sender_config": {"type_": "notify-send"}}
        config = sut.notification_config_builder.build(d)
        assert config == sut.DesktopNotifierConfig(
            sender_config=desktop_notifier.NotifySendNotifierConfig()
        )
