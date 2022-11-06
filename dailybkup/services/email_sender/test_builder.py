from dailybkup.services.email_sender.config import (
    MockEmailSenderConfig,
    MailGunEmailSenderConfig,
)
import dailybkup.services.email_sender as sut


class TestEmailSenderBuild:
    def test_builds_mock_sender(self):
        config = MockEmailSenderConfig(directory="foo")
        environ = {}
        builder = sut.EmailSenderBuilder()
        sender = builder.build(config, environ)
        assert isinstance(sender, sut.MockEmailSender)

    def test_builds_mailgun_email_sender(self):
        config = MailGunEmailSenderConfig(base_url="http://foo", from_="bar@bar.bar")
        environ = {"DAILYBKUP_MAILGUN_API_KEY": "keeey"}
        builder = sut.EmailSenderBuilder()
        sender = builder.build(config, environ)
        assert isinstance(sender, sut.MailGunEmailSender)
