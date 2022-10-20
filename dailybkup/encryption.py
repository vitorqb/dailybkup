from typing import Optional
from abc import ABC, abstractmethod
import dailybkup.state as statemod
import dailybkup.fileutils as fileutils
from dailybkup import config as configmod
from dailybkup import gpgutils
from dailybkup.phases import Phase
import dailybkup.fileutils as fileutils
import dataclasses
import logging


LOGGER = logging.getLogger(__name__)


class IEncryptor(ABC):
    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        ...


class PasswordEncryptor(IEncryptor):

    def __init__(
            self,
            config: configmod.PasswordEncryptionConfig,
            tempFileGenerator: fileutils.ITempFileGenerator,
    ):
        self._config = config
        self._tempFileGenerator = tempFileGenerator

    def run(self, state: statemod.State) -> statemod.State:
        assert state.current_file, "Missing current file for encryption"
        outfile = self._tempFileGenerator.gen_name()
        LOGGER.info("Starting encryption to %s",  outfile)
        gpgutils.encrypt(state.current_file, self._config.password, outfile)
        return dataclasses.replace(
            state,
            last_phase=Phase.ENCRYPTION,
            encrypted_file=outfile,
            current_file=outfile,
        )


class NoOpEncryptor(IEncryptor):
    def run(self, state: statemod.State) -> statemod.State:
        return dataclasses.replace(state, last_phase=Phase.ENCRYPTION)
