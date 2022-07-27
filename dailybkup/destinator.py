from abc import ABC, abstractmethod
import dataclasses
import dailybkup.state as statemod
import dailybkup.config as configmod
from dailybkup.phases import Phase
import shutil


class IDestinator(ABC):
    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        raise NotImplementedError()


class FileDestinator():

    _config: configmod.FileDestinationConfig

    def __init__(self, config: configmod.FileDestinationConfig):
        self._config = config

    def run(self, state: statemod.State) -> statemod.State:
        assert state.compressed_file is not None, "State has no compressed file"
        src = state.compressed_file
        dst = self._config.path
        shutil.copyfile(src, dst)
        return dataclasses.replace(state, last_phase=Phase.STORAGE)


def build_from_config(config: configmod.IDestinationConfig):
    if isinstance(config, configmod.FileDestinationConfig):
        return FileDestinator(config)
