from abc import ABC, abstractmethod
from dailybkup.state import State
import dataclasses
from typing import List
import logging
import dailybkup.compression.config as configmod
from dailybkup.phases import Phase
from typing import Any
import dailybkup.tarutils as tarutils
import dailybkup.fileutils as fileutils


LOGGER = logging.getLogger(__name__)


class ICompressor(ABC):

    _config: configmod.CompressionConfig
    _tempFileGenerator: fileutils.ITempFileGenerator

    def __init__(
        self,
        config: configmod.CompressionConfig,
        tempFileGenerator: fileutils.ITempFileGenerator,
    ) -> None:
        self._config = config
        self._tempFileGenerator = tempFileGenerator

    @abstractmethod
    def run(self, state: State) -> State:
        raise NotImplementedError()


class TarCompressor(ICompressor):
    def run(self, state: State) -> State:
        # TODO logfile cleanup
        logfile = self._tempFileGenerator.gen_name()
        destfile = self._tempFileGenerator.gen_name()
        tarutils.compress(
            files=self._config.files,
            destfile=destfile,
            logfile=logfile,
            excludes=self._config.exclude,
            tar_executable=self._config.tar_executable,
        )
        files = tarutils.list_files(destfile)
        new_state = dataclasses.replace(
            state,
            last_phase=Phase.COMPRESSION,
            files=files,
            compression_logfile=logfile,
            compressed_file=destfile,
            current_file=destfile,
        )
        LOGGER.info(f"Compression done to file {destfile}")
        LOGGER.info(f"Logs saved to file {logfile}")
        return new_state


class MockCompressor(ICompressor):
    def __init__(
        self,
        config: configmod.CompressionConfig,
        tempFileGenerator: fileutils.ITempFileGenerator,
    ) -> None:
        super().__init__(config, tempFileGenerator)
        self.calls: List[Any] = []

    def run(self, state: State) -> State:
        self.calls.append(state)
        return dataclasses.replace(state, last_phase=Phase.COMPRESSION, files=["foo"])
