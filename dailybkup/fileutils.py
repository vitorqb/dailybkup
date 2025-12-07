import abc
import tempfile
import os
from typing import Optional


class ITempFileGenerator(abc.ABC):
    @abc.abstractmethod
    def gen_name(self) -> str:
        ...


class TempFileGenerator(ITempFileGenerator):

    _directory: Optional[str]

    def __init__(self, directory: Optional[str] = None):
        self._directory = directory

    def gen_name(self) -> str:
        return tempfile.NamedTemporaryFile(dir=self._directory).name


def read_as_str(f: str) -> str:
    with open(f) as f_:
        return f_.read()


def write_str(f: str, x: str) -> None:
    with open(f, "wb") as f_:
        f_.write(x.encode())


def count_lines(f: str) -> int:
    with open(f) as f_:
        return len(f_.readlines())
