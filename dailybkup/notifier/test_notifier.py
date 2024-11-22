from unittest import mock
import dailybkup.notifier.notifier as sut
from dailybkup import state as statemod
from dailybkup.state import Phase
from dailybkup.services import email_sender as email_sender_mod
from dailybkup.services import desktop_notifier as desktop_notifier_mod
import dailybkup.state.mutations as m


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
        # Should not modify last phase
        assert final_state.last_phase == initial_state.last_phase


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


class TestDesktopNotifier:
    def test_send_desktop_notification_success(self):
        state = statemod.State.initial_state()
        petition = desktop_notifier_mod.DesktopNotificationPetition(
            summary="Backup completed!",
            body="Your backup has finished!",
        )
        sender = mock.Mock()
        notifier = sut.DesktopNotifier(sender=sender)
        newstate = notifier.run(state)
        sender.send.assert_called_once_with(petition)
        assert newstate == state

    def test_send_desktop_notification_error(self):
        state = statemod.State.initial_state().mutate(m.with_error(RuntimeError("FOO")))
        petition = desktop_notifier_mod.DesktopNotificationPetition(
            summary="Backup Failed!",
            body="Something has failed during your backup! =(",
        )
        sender = mock.Mock()
        notifier = sut.DesktopNotifier(sender=sender)
        newstate = notifier.run(state)
        sender.send.assert_called_once_with(petition)
        assert newstate == state
