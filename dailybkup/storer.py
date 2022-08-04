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
        assert state.current_file is not None, "State has no current file"
        dst = self._config.path
        LOGGER.info("Copying %s to %s", state.current_file, dst)
        shutil.copyfile(state.current_file, dst)
        return dataclasses.replace(state, last_phase=Phase.STORAGE)


def build_from_config(config: configmod.IStorageConfig):
    if isinstance(config, configmod.FileStorageConfig):
        return FileStorer(config)
