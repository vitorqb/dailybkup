from abc import ABC, abstractmethod
import dailybkup.state as statemod
import dailybkup.fileutils as fileutils
from dailybkup import gpgutils
from dailybkup.state import Phase
from dailybkup.encryption import config as configmod
import dailybkup.state.mutations as m
import dataclasses
import logging


LOGGER = logging.getLogger(__name__)


class Encryptor(ABC):
    def should_run(self, state: statemod.State) -> bool:
        return state.error is None

    def get_phase(self) -> Phase:
        return Phase.ENCRYPTION

    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State: ...


class PasswordEncryptor(Encryptor):
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
        LOGGER.info("Starting encryption to %s", outfile)
        gpgutils.encrypt(state.current_file, self._config.password, outfile)
        return state.mutate(
            m.with_encrypted_file(outfile),
            m.with_current_file(outfile),
        )


class NoOpEncryptor(Encryptor):
    def run(self, state: statemod.State) -> statemod.State:
        return state
