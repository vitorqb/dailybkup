from abc import ABC, abstractmethod
from dailybkup.state import State
import dataclasses
from typing import List
import tempfile
import subprocess
from dailybkup.phases import Phase
from typing import Any


@dataclasses.dataclass(frozen=True, kw_only=True)
class CompressorConfig():
    files: List[str]
    exclude: List[str]
    tar_executable: str = "tar"


class ICompressor(ABC):

    def __init__(self, config: CompressorConfig) -> None:
        self._config = config

    @abstractmethod
    def run(self, state: State) -> State:
        raise NotImplementedError()


class TarCompressor(ICompressor):

    def run(self, state: State) -> State:
        tar_executable = self._config.tar_executable
        # TODO logfile cleanup
        logfile = tempfile.NamedTemporaryFile().name
        compressed_file = tempfile.NamedTemporaryFile().name
        cmd = [tar_executable, "--dereference", "--checkpoint=1000", f"--index-file={logfile}", "-v", "-z", "-c", f"-f{compressed_file}"]
        for f in self._config.exclude:
            cmd.append(f"--exclude={f}")
        for f in self._config.files:
            cmd.append(f)
        subprocess.check_output(cmd)
        list_files_cmd = [tar_executable, "-zt", f"-f{compressed_file}"]
        files = subprocess.check_output(list_files_cmd).decode().splitlines()
        new_state = dataclasses.replace(
            state,
            last_phase=Phase.COMPRESSION,
            files=files,
            compression_logfile=logfile,
            compressed_file=compressed_file
        )
        return new_state


class MockCompressor(ICompressor):

    def __init__(self, config: CompressorConfig) -> None:
        super().__init__(config)
        self.calls: List[Any] = []

    def run(self, state: State) -> State:
        self.calls.append(state)
        return dataclasses.replace(state, last_phase=Phase.COMPRESSION, files=["foo"])
