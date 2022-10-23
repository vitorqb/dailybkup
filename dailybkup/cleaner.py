from abc import ABC, abstractmethod
import dailybkup.state as statemod
import dataclasses
from dailybkup.phases import Phase
import dailybkup.config as configmod
import dailybkup.b2utils as b2utils
from typing import Optional, Callable, Sequence
import logging


class ICleaner(ABC):
    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        ...


class B2Cleaner(ICleaner):

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
        return dataclasses.replace(state, last_phase=Phase.CLEANUP)


class NoOpCleaner(ICleaner):
    def run(self, state: statemod.State) -> statemod.State:
        return dataclasses.replace(state, last_phase=Phase.CLEANUP)


class CompositeCleaner(ICleaner):

    _cleaners: Sequence[ICleaner]
    _logging: logging.Logger = logging.getLogger(__name__ + ".CompositeCleaner")

    def __init__(self, cleaners: Sequence[ICleaner]):
        self._cleaners = cleaners

    def run(self, state: statemod.State) -> statemod.State:
        final_state = state
        for cleaner in self._cleaners:
            self._logging.info("Running cleaner {cleaner}")
            final_state = cleaner.run(final_state)
        final_state = dataclasses.replace(final_state, last_phase=Phase.CLEANUP)
        return final_state
