import abc
import dailybkup.state as statemod
import dailybkup.services.email_sender as email_sender_mod
import dailybkup.state.mutations as m
import dailybkup.services.desktop_notifier as desktop_notifier_mod
import logging
from dailybkup.state import Phase
from typing import Sequence


LOGGER = logging.getLogger(__name__)


class Notifier(abc.ABC):
    def should_run(self, state: statemod.State) -> bool:
        # Should always run, since notifies success or failures!
        return True

    def get_phase(self) -> Phase:
        return Phase.NOTIFICATION

    @abc.abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        ...


class _EmailPetitionBuilder:
    def __init__(self, recipient_address: str):
        self._recipient_address = recipient_address

    def build(self, state: statemod.State) -> email_sender_mod.EmailPetition:
        if state.error:
            return self.build_error()
        return self.build_success()

    def build_success(self) -> email_sender_mod.EmailPetition:
        return email_sender_mod.EmailPetition(
            recipient_address=self._recipient_address,
            subject="Backup completed!",
            body="Your backup has finished!",
        )

    def build_error(self) -> email_sender_mod.EmailPetition:
        return email_sender_mod.EmailPetition(
            recipient_address=self._recipient_address,
            subject="Backup Failed!",
            body="Something has failed during your backup! =(",
        )


class EmailNotifier(Notifier):
    def __init__(
        self,
        sender: email_sender_mod.PEmailSender,
        recipient_address: str,
    ):
        self.sender = sender
        self._email_petition_builder = _EmailPetitionBuilder(recipient_address)

    def run(self, state: statemod.State) -> statemod.State:
        email_petition = self._email_petition_builder.build(state)
        logging.info("Sending email: %s", email_petition)
        self.sender.send(email_petition)
        return state


class _DesktopPetitionBuilder:
    def build(
        self, state: statemod.State
    ) -> desktop_notifier_mod.DesktopNotificationPetition:
        if state.error:
            return self._build_error(state)
        return self._build_success(state)

    def _build_error(
        self, state: statemod.State
    ) -> desktop_notifier_mod.DesktopNotificationPetition:
        return desktop_notifier_mod.DesktopNotificationPetition(
            summary="Backup Failed!",
            body="Something has failed during your backup! =(",
        )

    def _build_success(
        self, state: statemod.State
    ) -> desktop_notifier_mod.DesktopNotificationPetition:
        return desktop_notifier_mod.DesktopNotificationPetition(
            summary="Backup completed!",
            body="Your backup has finished!",
        )


class DesktopNotifier(Notifier):
    def __init__(self, sender: desktop_notifier_mod.PDesktopNotifier):
        self._sender = sender
        self._petition_builder = _DesktopPetitionBuilder()

    def run(self, state: statemod.State) -> statemod.State:
        petition = self._petition_builder.build(state)
        logging.info("Sending desktop notification: %s", petition)
        self._sender.send(petition)
        return state


class CompositeNotifier(Notifier):
    def __init__(self, notifiers: Sequence[Notifier]):
        self._notifiers = notifiers

    def run(self, state: statemod.State) -> statemod.State:
        final_state = state
        for notifier in self._notifiers:
            final_state = notifier.run(final_state)
        return final_state
