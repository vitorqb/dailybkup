from abc import ABC, abstractmethod
import dailybkup.state as statemod
from dailybkup.state import Phase
import dailybkup.cleaner.config as configmod
import dailybkup.b2utils as b2utils
from typing import Sequence
from typing import TYPE_CHECKING
import logging
import dailybkup.state.mutations as m

if TYPE_CHECKING:
    import dailybkup.gdrive_utils as gdrive_utils


class Cleaner(ABC):
    def should_run(self, state: statemod.State) -> bool:
        return state.error is None

    def get_phase(self) -> Phase:
        return Phase.CLEANUP

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
        return state


class GDriveCleaner(Cleaner):
    def __init__(
        self, config: configmod.GDriveCleanerConfig, client: "gdrive_utils.GDriveClient"
    ):
        self._config = config
        self._client = client

    def run(self, state: statemod.State) -> statemod.State:
        folder_id = self._config.folder_id
        prefix = self._config.prefix
        retain_last = self._config.retain_last
        files = sorted(
            (
                x
                for x in self._client.get_files(parent_id=folder_id)
                if x.name.startswith(prefix)
            ),
            key=lambda x: x.name,
        )
        files_to_delete = files[:-retain_last]
        self._client.delete_batch([x.id for x in files_to_delete])
        return state


class NoOpCleaner(Cleaner):
    def run(self, state: statemod.State) -> statemod.State:
        return state


class CompositeCleaner(Cleaner):

    _cleaners: Sequence[Cleaner]
    _logging: logging.Logger = logging.getLogger(__name__ + ".CompositeCleaner")

    def __init__(self, cleaners: Sequence[Cleaner]):
        self._cleaners = cleaners

    def run(self, state: statemod.State) -> statemod.State:
        final_state = state
        for cleaner in self._cleaners:
            self._logging.info(f"Running cleaner {cleaner}")
            final_state = cleaner.run(final_state)
        return final_state
