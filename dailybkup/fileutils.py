import abc
import tempfile
from typing import Optional


class ITempFileGenerator(abc.ABC):
    def gen_name(self) -> str:
        ...


class TempFileGenerator(ITempFileGenerator):

    _directory: Optional[str]

    def __init__(self, directory: Optional[str] = None):
        self._directory = directory

    def gen_name(self) -> str:
        return tempfile.NamedTemporaryFile(dir=self._directory).name
