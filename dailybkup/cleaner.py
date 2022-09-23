from abc import ABC, abstractmethod
import dailybkup.state as statemod
import dataclasses
from dailybkup.phases import Phase
import dailybkup.config as configmod
import dailybkup.b2utils as b2utils


class ICleaner(ABC):

    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        ...


class B2Cleaner(ICleaner):

    _b2context: b2utils.B2Context
    _config: configmod.B2CleanerConfig

    def __init__(
            self,
            config: configmod.B2CleanerConfig,
            *,
            b2context: b2utils.B2Context
    ):
        self._config = config
        self._b2context = b2context

    def run(self, state: statemod.State) -> statemod.State:
        retain_last = self._config.retain_last
        files = sorted(self._b2context.get_file_names())
        files_to_delete = files[:-retain_last]
        for file_to_delete in files_to_delete:
            self._b2context.delete(file_to_delete)
        return dataclasses.replace(state, last_phase=Phase.CLEANUP)
