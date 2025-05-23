from abc import ABC, abstractmethod
import dailybkup.state as statemod
from typing import List
import logging
import dailybkup.compression.config as configmod
from dailybkup.state import Phase
from typing import Any
import dailybkup.tarutils as tarutils
import dailybkup.fileutils as fileutils
import dailybkup.state.mutations as m


LOGGER = logging.getLogger(__name__)


class Compressor(ABC):
    def should_run(self, state: statemod.State) -> bool:
        return state.error is None

    def get_phase(self) -> Phase:
        return Phase.COMPRESSION

    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        raise NotImplementedError()


class TarCompressor(Compressor):
    def __init__(
        self,
        config: configmod.CompressionConfig,
        *,
        tempFileGenerator: fileutils.ITempFileGenerator,
        tar_compressor_runner: tarutils.TarCompressorRunner,
    ) -> None:
        self._config = config
        self._tempFileGenerator = tempFileGenerator
        self._tar_compressor_runner = tar_compressor_runner

    def run(self, state: statemod.State) -> statemod.State:
        # TODO logfile cleanup
        logfile = self._tempFileGenerator.gen_name()
        destfile = self._tempFileGenerator.gen_name()
        self._tar_compressor_runner(
            files=self._config.files,
            destfile=destfile,
            logfile=logfile,
            excludes=self._config.exclude,
            tar_executable=self._config.tar_executable,
        )
        files = [x for x in tarutils.list_files(destfile)]
        LOGGER.info(f"Compression done to file {destfile}")
        LOGGER.info(f"Logs saved to file {logfile}")
        return state.mutate(
            m.with_files(files),
            m.with_compression_logfile(logfile),
            m.with_compressed_file(destfile),
            m.with_current_file(destfile),
        )


class MockCompressor(Compressor):
    def __init__(
        self,
        config: configmod.CompressionConfig,
        tempFileGenerator: fileutils.ITempFileGenerator,
    ) -> None:
        self._config = config
        self._tempFileGenerator = tempFileGenerator
        self.calls: List[Any] = []

    def run(self, state: statemod.State) -> statemod.State:
        self.calls.append(state)
        return state.mutate(
            m.with_files(["foo"]),
        )
