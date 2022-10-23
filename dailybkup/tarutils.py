from typing import Sequence
import subprocess
import logging


LOGGER = logging.getLogger(__name__)
TAR_FLAGS = ["--dereference", "--checkpoint=1000", "-v", "-z", "-c"]


def compress(
    *,
    files: Sequence[str],
    destfile,
    logfile: str = None,
    excludes: Sequence[str] = [],
    tar_executable: str = "tar",
) -> None:
    cmd = [tar_executable, *TAR_FLAGS, f"-f{destfile}"]
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
