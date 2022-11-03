from unittest import mock
import pytest

import dailybkup.testutils as testutils
from . import builder as sut
import dailybkup.services.email_sender as email_sender_mod
from .config import EmailNotifierConfig
from .notifier import EmailNotifier


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
            builder = sut.NotifierBuilder(email_sender_builder=email_sender_builder)
            notifier = builder.build(config)
            assert isinstance(notifier, EmailNotifier)
            assert isinstance(notifier.sender, email_sender_mod.MockEmailSender)

    def test_fails_if_unknown_config_class(self):
        config = mock.Mock()
        builder = sut.NotifierBuilder(email_sender_builder=mock.Mock())
        with pytest.raises(ValueError):
            builder.build(config)
