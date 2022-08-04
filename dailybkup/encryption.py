from typing import Optional
from abc import ABC, abstractmethod
import dailybkup.state as statemod
from dailybkup import config as configmod
from dailybkup import gpgutils
from dailybkup.phases import Phase
import tempfile
import dataclasses
import logging


LOGGER = logging.getLogger(__name__)


class IEncryptor(ABC):
    @abstractmethod
    def run(self, state: statemod.State) -> statemod.State:
        ...


class PasswordEncryptor(IEncryptor):

    def __init__(self, config: configmod.PasswordEncryptionConfig):
        self._config = config

    def run(self, state: statemod.State) -> statemod.State:
        assert state.current_file, "Missing current file for encryption"
        outfile = tempfile.NamedTemporaryFile().name
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


def build_from_config(config: Optional[configmod.IEncryptionConfig]) -> IEncryptor:
    if config is None:
        return NoOpEncryptor()
    if isinstance(config, configmod.PasswordEncryptionConfig):
        return PasswordEncryptor(config)
    raise ValueError(f"Unknown encryptor config: {config}")
