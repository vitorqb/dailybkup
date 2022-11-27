from abc import ABC, abstractmethod
import dailybkup.state as statemod
import dataclasses
from dailybkup.state import Phase
import dailybkup.cleaner.config as configmod
import dailybkup.b2utils as b2utils
from typing import Sequence
import logging
import dailybkup.state.mutations as m


class Cleaner(ABC):
    def should_run(self, state: statemod.State) -> bool:
        return state.error is None

    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        ...


class B2Cleaner(Cleaner):

    _b2context: b2utils.B2Context
    _config: configmod.B2CleanerConfig
    LOGGER: logging.Logger = logging.getLogger("B2Cleaner")

    def __init__(
        self, config: configmod.B2CleanerConfig, *, b2context: b2utils.B2Context
    ):
        self._config = config
        self._b2context = b2context

    def run(self, state: statemod.State) -> statemod.State:
        retain_last = self._config.retain_last
        files = sorted(self._b2context.get_file_names())
        files_to_delete = files[:-retain_last]
        for file_to_delete in files_to_delete:
            self.LOGGER.info(
                "Deleting file %s from bucket %s",
                file_to_delete,
                self._b2context.bucket_name,
            )
            self._b2context.delete(file_to_delete)
        return state.mutate(m.with_last_phase(Phase.CLEANUP))


class NoOpCleaner(Cleaner):
    def run(self, state: statemod.State) -> statemod.State:
        return state.mutate(m.with_last_phase(Phase.CLEANUP))


class CompositeCleaner(Cleaner):

    _cleaners: Sequence[Cleaner]
    _logging: logging.Logger = logging.getLogger(__name__ + ".CompositeCleaner")

    def __init__(self, cleaners: Sequence[Cleaner]):
        self._cleaners = cleaners

    def run(self, state: statemod.State) -> statemod.State:
        final_state = state
        for cleaner in self._cleaners:
            self._logging.info("Running cleaner {cleaner}")
            final_state = cleaner.run(final_state)
        return final_state.mutate(m.with_last_phase(Phase.CLEANUP))
