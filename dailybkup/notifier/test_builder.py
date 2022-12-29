from unittest import mock
import pytest

import dailybkup.testutils as testutils
from . import builder as sut
import dailybkup.services.email_sender as email_sender_mod
import dailybkup.services.desktop_notifier as desktop_notifier_mod
from .config import EmailNotifierConfig, DesktopNotifierConfig
from .notifier import EmailNotifier, DesktopNotifier


class TestNotifierBuilder:
    def test_build_with_mock_email_sender(self):
        with testutils.with_temp_dir() as temp_dir:
            email_sender_builder = email_sender_mod.EmailSenderBuilder()
            sender_config = email_sender_mod.MockEmailSenderConfig(directory=temp_dir)
            config = EmailNotifierConfig(
                type_="email",
                recipient_address="foo@bar.baz",
                sender_config=sender_config,
            )
            builder = sut.NotifierBuilder(
                email_sender_builder=email_sender_builder,
                desktop_notifier_builder=mock.Mock(),
            )
            notifier = builder.build(config)
            assert isinstance(notifier, EmailNotifier)
            assert isinstance(notifier.sender, email_sender_mod.MockEmailSender)

    def test_build_with_notify_sender_notifier(self):
        desktop_notifier_builder = desktop_notifier_mod.DesktopNotifierBuilder()
        notifier_config = desktop_notifier_mod.NotifySendNotifierConfig()
        config = DesktopNotifierConfig(sender_config=notifier_config)
        email_sender_builder = mock.Mock()
        builder = sut.NotifierBuilder(
            email_sender_builder=email_sender_builder,
            desktop_notifier_builder=desktop_notifier_builder,
        )
        notifier = builder.build(config)
        assert isinstance(notifier, DesktopNotifier)
        assert isinstance(notifier._sender, desktop_notifier_mod.NotifySendNotifier)

    def test_fails_if_unknown_config_class(self):
        config = mock.Mock()
        builder = sut.NotifierBuilder(mock.Mock(), mock.Mock())
        with pytest.raises(ValueError):
            builder.build(config)
