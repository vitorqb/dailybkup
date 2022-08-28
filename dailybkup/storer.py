from abc import ABC, abstractmethod
import dataclasses
import dailybkup.state as statemod
import dailybkup.config as configmod
from dailybkup.phases import Phase
import shutil
import logging
import datetime
from typing import Callable
import dailybkup.b2utils as b2utils
from typing import Sequence


LOGGER = logging.getLogger(__name__)


class IStorer(ABC):
    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        ...


class CompositeStorer(IStorer):

    _storers: Sequence[IStorer]
    _logging: logging.Logger = logging.getLogger(__name__ + '.CompositeStorer')

    def __init__(self, storers: Sequence[IStorer]):
        self._storers = storers

    def run(self, state: statemod.State) -> statemod.State:
        final_state = state
        for storer in self._storers:
            self._logging.info(f"Running storer {storer}")
            final_state = storer.run(final_state)
        final_state = dataclasses.replace(
            final_state,
            last_phase=Phase.STORAGE,
            current_file=None,
        )
        return final_state


class FileStorer(IStorer):

    _config: configmod.FileStorageConfig

    def __init__(self, config: configmod.FileStorageConfig):
        self._config = config

    def run(self, state: statemod.State) -> statemod.State:
        assert state.current_file is not None, "State has no current file"
        dst = self._config.path
        LOGGER.info("Copying %s to %s", state.current_file, dst)
        shutil.copyfile(state.current_file, dst)
        return dataclasses.replace(state, last_phase=Phase.STORAGE)


class B2Storer(IStorer):

    _config: configmod.B2StorageConfig

    def __init__(
            self,
            config: configmod.B2StorageConfig,
            b2context: b2utils.B2Context,
    ):
        self._config = config
        self._b2context = b2context

    def run(self, state: statemod.State) -> statemod.State:
        assert state.current_file, "No current file to upload!"
        src = state.current_file
        bucket = self._b2context.bucket_name
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        file_name = f"{datetime_str}{self._config.suffix}"
        LOGGER.info("Copying %s to %s in bucket %s", src, file_name, bucket)
        self._b2context.upload(src, file_name)
        return dataclasses.replace(state, last_phase=Phase.STORAGE)


def build_from_config(
        config: configmod.IStorageConfig,
        l_b2context: Callable[[str], b2utils.B2Context],
):
    if isinstance(config, configmod.FileStorageConfig):
        return FileStorer(config)
    if isinstance(config, configmod.B2StorageConfig):
        b2context = l_b2context(config.bucket)
        return B2Storer(config, b2context)
    raise RuntimeError(f"Uknown config class: {config}")
