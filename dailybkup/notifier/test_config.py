import dailybkup.notifier.config as sut
import dailybkup.services.email_sender as email_sender


class TestNotificationConfigBuilder:
    def test_build(self):
        d = {
            "type_": "email",
            "recipient_address": "foo@bar.baz",
            "sender_config": {"type_": "mock", "directory": "./foo"},
        }
        config = sut.NotificationConfigBuilder().build(d)
        assert config == sut.EmailNotifierConfig(
            recipient_address="foo@bar.baz",
            sender_config=email_sender.MockEmailSenderConfig(directory="./foo"),
        )
