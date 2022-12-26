from typing import Sequence
import subprocess
import logging
from typing import Optional


LOGGER = logging.getLogger(__name__)


class TarCompressorRunner:
    def __init__(
        self, *, executable: str = "tar", flags: Optional[Sequence[str]] = None
    ):
        self._executable = executable
        self._flags = flags or []

    def __call__(
        self,
        *,
        files: Sequence[str],
        destfile: str,
        logfile: Optional[str] = None,
        excludes: Optional[Sequence[str]] = None,
        tar_executable: str = "tar",
    ):
        excludes = excludes or []
        cmd = [self._executable, *self._flags, "-c", f"-f{destfile}"]
        if logfile:
            cmd.append(f"--index-file={logfile}")
        for exclude in excludes:
            cmd.append(f"--exclude={exclude}")
        for file_ in files:
            cmd.append(file_)
        LOGGER.info(f"Running: {cmd}")
        subprocess.check_output(cmd)


def list_files(tar_file: str) -> Sequence[str]:
    output = subprocess.check_output(["tar", "-tf", tar_file])
    return output.decode().splitlines()
