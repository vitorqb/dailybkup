from dailybkup.services.email_sender.config import (
    MockEmailSenderConfig,
    MailGunEmailSenderConfig,
)
import dailybkup.services.email_sender as sut


class TestEmailSenderBuild:
    def test_builds_mock_sender(self):
        config = MockEmailSenderConfig(directory="foo")
        builder = sut.EmailSenderBuilder()
        sender = builder.build(config)
        assert isinstance(sender, sut.MockEmailSender)

    def test_builds_mailgun_email_sender(self):
        config = MailGunEmailSenderConfig(
            base_url="http://foo",
            from_="bar@bar.bar",
            api_key="keeey",
        )
        builder = sut.EmailSenderBuilder()
        sender = builder.build(config)
        assert isinstance(sender, sut.MailGunEmailSender)
