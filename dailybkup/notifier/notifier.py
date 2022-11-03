import abc
import dataclasses
import dailybkup.pipeline as pipeline
import dailybkup.state as statemod
import dailybkup.services.email_sender as email_sender_mod
from dailybkup.phases import Phase
from typing import Sequence


class INotifier(abc.ABC, pipeline.IRunnable):
    pass


class EmailNotifier(INotifier):
    def __init__(
        self,
        sender: email_sender_mod.PEmailSender,
        recipient_address: str,
    ):
        self.sender = sender
        self._recipient_address = recipient_address

    def run(self, state: statemod.State) -> statemod.State:
        email_petition = email_sender_mod.EmailPetition(
            recipient_address=self._recipient_address,
            subject="Backup completed!",
            body="Your backup has finished!",
        )
        self.sender.send(email_petition)
        return state


class CompositeNotifier(INotifier):
    def __init__(self, notifiers: Sequence[INotifier]):
        self._notifiers = notifiers

    def run(self, state: statemod.State) -> statemod.State:
        final_state = state
        for notifier in self._notifiers:
            final_state = notifier.run(final_state)
        return dataclasses.replace(final_state, last_phase=Phase.NOTIFICATION)
