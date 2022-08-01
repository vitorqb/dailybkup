from abc import ABC, abstractmethod
import dataclasses
import dailybkup.state as statemod
import dailybkup.config as configmod
from dailybkup.phases import Phase
import shutil
import logging


LOGGER = logging.getLogger(__name__)


class IStorer(ABC):
    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        ...


class FileStorer(IStorer):

    _config: configmod.FileStorageConfig

    def __init__(self, config: configmod.FileStorageConfig):
        self._config = config

    def run(self, state: statemod.State) -> statemod.State:
        assert state.compressed_file is not None, "State has no compressed file"
        src = state.encrypted_file if state.encrypted_file else state.compressed_file
        dst = self._config.path
        LOGGER.info("Copying %s to %s", src, dst)
        shutil.copyfile(src, dst)
        return dataclasses.replace(state, last_phase=Phase.STORAGE)


def build_from_config(config: configmod.IStorageConfig):
    if isinstance(config, configmod.FileStorageConfig):
        return FileStorer(config)
