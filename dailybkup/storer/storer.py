from abc import ABC, abstractmethod
import os
import dailybkup.state as statemod
import dailybkup.storer.config as configmod
import dailybkup.state.mutations as m
from dailybkup.state import Phase
import shutil
import logging
import datetime
from typing import Callable, Sequence
import dailybkup.b2utils as b2utils

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import dailybkup.gdrive_utils as gdrive_utils


LOGGER = logging.getLogger(__name__)


class IBackupFileNameGenerator(ABC):
    def __init__(self, *, suffix: str, now_fn: Callable[[], datetime.datetime]):
        self._suffix = suffix
        self._now_fn = now_fn

    @abstractmethod
    def generate(self) -> str:
        ...


class BackupFileNameGenerator(IBackupFileNameGenerator):
    def generate(self) -> str:
        formatted_now = self._now_fn().strftime("%Y-%m-%dT%H:%M:%S")
        return f"{formatted_now}{self._suffix}"


class Storer(ABC):
    def should_run(self, state: statemod.State) -> bool:
        return state.error is None

    def get_phase(self) -> Phase:
        return Phase.STORAGE

    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        ...


class CompositeStorer(Storer):

    _storers: Sequence[Storer]
    _logging: logging.Logger = logging.getLogger(__name__ + ".CompositeStorer")

    def __init__(self, storers: Sequence[Storer]):
        self._storers = storers

    def run(self, state: statemod.State) -> statemod.State:
        final_state = state
        for storer in self._storers:
            self._logging.info(f"Running storer {storer}")
            final_state = storer.run(final_state)
        return final_state.mutate(m.with_current_file(None))


class FileStorer(Storer):

    _config: configmod.FileStorageConfig

    def __init__(
        self,
        config: configmod.FileStorageConfig,
        backup_file_name_generator: IBackupFileNameGenerator,
    ):
        self._config = config
        self._backup_file_name_generator = backup_file_name_generator

    def run(self, state: statemod.State) -> statemod.State:
        assert state.current_file is not None, "State has no current file"
        dst = os.path.join(
            self._config.directory,
            self._backup_file_name_generator.generate(),
        )
        LOGGER.info("Copying %s to %s", state.current_file, dst)
        shutil.copyfile(state.current_file, dst)
        return state


class B2Storer(Storer):

    _config: configmod.B2StorageConfig
    _b2context: b2utils.B2Context
    _backup_file_name_generator: IBackupFileNameGenerator

    def __init__(
        self,
        config: configmod.B2StorageConfig,
        b2context: b2utils.B2Context,
        backup_file_name_generator: IBackupFileNameGenerator,
    ):
        self._config = config
        self._b2context = b2context
        self._backup_file_name_generator = backup_file_name_generator

    def run(self, state: statemod.State) -> statemod.State:
        assert state.current_file, "No current file to upload!"
        src = state.current_file
        bucket = self._b2context.bucket_name
        file_name = self._backup_file_name_generator.generate()
        LOGGER.info("Copying %s to %s in bucket %s", src, file_name, bucket)
        self._b2context.upload(src, file_name)
        return state


class GDriveStorer(Storer):
    def __init__(
        self,
        config: configmod.GDriveStorerConfig,
        client: "gdrive_utils.GDriveClient",
        backup_file_name_generator: IBackupFileNameGenerator,
    ):
        self._config = config
        self._client = client
        self._backup_file_name_generator = backup_file_name_generator

    def run(self, state: statemod.State) -> statemod.State:
        assert state.current_file, "No current file to upload!"
        src = state.current_file
        parent_id = self._config.folder_id
        file_name = self._backup_file_name_generator.generate()
        LOGGER.info(
            "Copying %s to Google Drive: folder_id=%s filename=%s",
            src,
            parent_id,
            file_name,
        )
        self._client.upload(
            parent_id=parent_id, local_file_path=src, remote_file_name=file_name
        )
        return state
