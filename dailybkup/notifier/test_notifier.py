from unittest import mock
import dailybkup.notifier.notifier as sut
from dailybkup import state as statemod
from dailybkup.phases import Phase
from dailybkup.services import email_sender as email_sender_mod


class TestCompositeNotifier:
    def test_calls_all_notifiers(self):
        initial_state = statemod.State.initial_state()
        notifiers = [mock.Mock(), mock.Mock()]
        for notifier in notifiers:
            notifier.run.return_value = initial_state
        composite_notifier = sut.CompositeNotifier(notifiers)
        final_state = composite_notifier.run(initial_state)
        notifiers[0].run.assert_called_once()
        notifiers[1].run.assert_called_once()
        assert final_state.last_phase == Phase.NOTIFICATION


class TestEmailNotifier:
    def test_sends_email_petition(self):
        state = statemod.State.initial_state()
        sender = mock.Mock()
        recipient_address = "foo@bar.baz"
        email_petition = email_sender_mod.EmailPetition(
            recipient_address=recipient_address,
            subject="Backup completed!",
            body="Your backup has finished!",
        )
        notifier = sut.EmailNotifier(sender=sender, recipient_address=recipient_address)
        notifier.run(state)
        sender.send.assert_called_once_with(email_petition)
