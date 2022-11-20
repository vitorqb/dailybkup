import abc
import dataclasses
import logging
import os
from dailybkup.phases import Phase
from typing import List, Optional, Callable


StateMutation = Callable[["State"], "State"]


@dataclasses.dataclass(frozen=True, kw_only=True)
class State:
    last_phase: Phase = Phase.BEGIN
    files: Optional[List[str]] = None
    compression_logfile: Optional[str] = None
    compressed_file: Optional[str] = None
    encrypted_file: Optional[str] = None
    current_file: Optional[str] = None
    error: Optional[Exception] = None

    @classmethod
    def initial_state(cls, **kwargs) -> "State":
        return cls(**kwargs)

    def mutate(self, *mutations: StateMutation) -> "State":
        out = self
        for mutation in mutations:
            out = mutation(out)
        return out


class IPhaseTransitionHook(abc.ABC):
    """
    A hook that is run everytime the state transitions to one phase to
    another. It can both do side-effects or modify the state itself.
    """

    def should_run(self, old_state: State, new_state: State) -> bool:
        ...

    def run(self, state: State) -> State:
        ...


class CompressedFileCleanupHook(IPhaseTransitionHook):

    _logger = logging.getLogger(__name__ + ".CompressedFileCleanupHook")

    def should_run(self, old_state: State, new_state: State) -> bool:
        return (
            new_state.compressed_file is not None
            and old_state.last_phase == Phase.COMPRESSION
            and new_state.current_file != new_state.compressed_file
        )

    def run(self, state: State) -> State:
        if state.compressed_file is None:
            self._logger.info("Skipping deletion because state.compressed_file is None")
            return state
        self._logger.info("Deleting compressed file: %s", state.compressed_file)
        os.remove(state.compressed_file)
        return dataclasses.replace(state, compressed_file=None)


class EncryptedFileCleanupHook(IPhaseTransitionHook):

    _logger = logging.getLogger(__name__ + ".EncryptedFileCleanupHook")

    def should_run(self, old_state: State, new_state: State) -> bool:
        return (
            new_state.encrypted_file is not None
            and old_state.last_phase == Phase.ENCRYPTION
            and new_state.current_file != new_state.encrypted_file
        )

    def run(self, state: State) -> State:
        if state.encrypted_file is None:
            self._logger.info("Skipping deletion because state.encrypted_file is None")
            return state
        self._logger.info("Deleting encrypted file: %s", state.encrypted_file)
        os.remove(state.encrypted_file)
        return dataclasses.replace(state, encrypted_file=None)


class FinalFileCleanupHook(IPhaseTransitionHook):

    _logger = logging.getLogger(__name__ + ".FinalFileCleanupHook")

    def should_run(self, old_state: State, new_state: State) -> bool:
        return new_state.last_phase == Phase.END

    def run(self, state: State) -> State:
        new_state = state
        if state.compression_logfile is not None:
            self._logger.info(
                "Deleting compression log file: %s", state.compression_logfile
            )
            os.remove(state.compression_logfile)
            new_state = dataclasses.replace(state, compression_logfile=None)
        return new_state


class MockPhaseTransitionHook(IPhaseTransitionHook):

    _call_count: int
    _should_run: bool
    _last_state: Optional[State]

    def __init__(self, should_run: bool = True):
        self._call_count = 0
        self._should_run = should_run
        self._last_state = None

    def should_run(self, old_state: State, new_state: State) -> bool:
        return self._should_run

    def run(self, state: State) -> State:
        self._call_count += 1
        self._last_state = state
        return state

    @property
    def call_count(self) -> int:
        return self._call_count

    @property
    def last_state(self) -> Optional[State]:
        return self._last_state
