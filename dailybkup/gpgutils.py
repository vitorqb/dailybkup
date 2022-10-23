import subprocess
import logging


LOGGER = logging.getLogger(__name__)


class GPGExecutionFailed(Exception):
    pass


def encrypt(infile: str, password: str, outfile: str):
    # TODO Make gpg path configurable
    cmd = [
        "gpg",
        "--output",
        outfile,
        "--batch",
        "--yes",
        "--passphrase-fd",
        "0",
        "-c",
        infile,
    ]
    LOGGER.debug("Running: %s", cmd)
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    process.communicate(password.encode())
    if process.returncode != 0:
        raise GPGExecutionFailed(f"Command {cmd} exitted w/ code {process.returncode}")


def decrypt(infile: str, password: str, outfile: str):
    # TODO Make gpg path configurable
    cmd = [
        "gpg",
        "--output",
        outfile,
        "--batch",
        "--yes",
        "--passphrase-fd",
        "0",
        "-d",
        infile,
    ]
    LOGGER.debug("Running: %s", cmd)
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    process.communicate(password.encode())
    if process.returncode != 0:
        raise GPGExecutionFailed(f"Command {cmd} exitted w/ code {process.returncode}")
