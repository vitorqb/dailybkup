from dailybkup.services.email_sender.config import MockEmailSenderConfig
import dailybkup.services.email_sender as sut


class TestEmailSenderBuild:
    def test_builds_mock_sender(self):
        config = MockEmailSenderConfig(directory="foo")
        builder = sut.EmailSenderBuilder()
        sender = builder.build(config)
        assert isinstance(sender, sut.MockEmailSender)
