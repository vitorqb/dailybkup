import dataclasses
from dailybkup.phases import Phase
from typing import List, Optional
from .state import StateMutation


def with_last_phase(last_phase: Optional[Phase]) -> StateMutation:
    return lambda x: dataclasses.replace(x, last_phase=last_phase)


def with_files(files: List[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, files=files)


def with_compression_logfile(compression_logfile: Optional[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, compression_logfile=compression_logfile)


def with_compressed_file(compressed_file: Optional[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, compressed_file=compressed_file)


def with_encrypted_file(encrypted_file: Optional[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, encrypted_file=encrypted_file)


def with_current_file(current_file: Optional[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, current_file=current_file)


def with_error(error: Optional[Exception]) -> StateMutation:
    return lambda x: dataclasses.replace(x, error=error)
