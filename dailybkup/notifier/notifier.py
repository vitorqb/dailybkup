import abc
import dataclasses
import dailybkup.pipeline as pipeline
import dailybkup.state as statemod
import dailybkup.services.email_sender as email_sender_mod
import logging
from dailybkup.phases import Phase
from typing import Sequence


LOGGER = logging.getLogger(__name__)


class Notifier(abc.ABC):
    def should_run(self, state: statemod.State) -> bool:
        # Should always run, since notifies success or failures!
        return True

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


class CompositeNotifier(Notifier):
    def __init__(self, notifiers: Sequence[Notifier]):
        self._notifiers = notifiers

    def run(self, state: statemod.State) -> statemod.State:
        final_state = state
        for notifier in self._notifiers:
            final_state = notifier.run(final_state)
        return dataclasses.replace(final_state, last_phase=Phase.NOTIFICATION)
