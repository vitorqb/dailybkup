import dailybkup.state as statemod
import dailybkup.compression as compression
import dailybkup.storer as storermod
from dailybkup.phases import Phase
from dailybkup import encryption as encryptionmod
from typing import Sequence
import logging
import dataclasses


LOGGER = logging.getLogger(__name__)


class Runner():
    """
    Class responsible to run all phases of the backup.
    """

    def __init__(
            self,
            *,
            compressor: compression.ICompressor,
            storer: storermod.IStorer,
            encryptor: encryptionmod.IEncryptor,
            phase_transition_hooks: Sequence[statemod.IPhaseTransitionHook] = [],
    ):
        self._compressor: compression.ICompressor = compressor
        self._storer: storermod.IStorer = storer
        self._encryptor = encryptor
        self._phase_transition_hooks = phase_transition_hooks

    def run(self) -> statemod.State:
        state = statemod.State.initial_state()

        LOGGER.info("Running compression")
        state = self._run_phase_transition_hooks(state, self._compressor.run(state))

        LOGGER.info("Running encryptor")
        state = self._run_phase_transition_hooks(state, self._encryptor.run(state))

        LOGGER.info("Running storers")
        state = self._run_phase_transition_hooks(state, self._storer.run(state))

        # Is there a nicer way to do this?
        state_before_end = state
        state = dataclasses.replace(state_before_end, last_phase=Phase.END)
        self._run_phase_transition_hooks(state_before_end, state)

        LOGGER.info("Finished pipeline")
        return state

    def _run_phase_transition_hooks(
            self,
            old_state: statemod.State,
            new_state: statemod.State,
    ) -> statemod.State:
        final_state = new_state
        for hook in self._phase_transition_hooks:
            if hook.should_run(old_state, new_state):
                final_state = hook.run(final_state)
        return final_state
