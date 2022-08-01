import dailybkup.state as statemod
import dailybkup.compression as compression
import dailybkup.storer as storermod
from dailybkup import encryption as encryptionmod
from typing import Sequence
import logging


LOGGER = logging.getLogger(__name__)


class Runner():
    """
    Class responsible to run all phases of the backup.
    """

    def __init__(
            self,
            *,
            compressor: compression.ICompressor,
            storers: Sequence[storermod.IStorer],
            encryptor: encryptionmod.IEncryptor,
    ):
        self._compressor: compression.ICompressor = compressor
        self._storers: Sequence[storermod.IStorer] = storers
        self._encryptor = encryptor

    def run(self) -> statemod.State:
        state = statemod.State.initial_state()

        LOGGER.info("Running compression")
        state = self._compressor.run(state)

        LOGGER.info("Running encryptor")
        state = self._encryptor.run(state)

        LOGGER.info("Running storers")
        for storer in self._storers:
            state = storer.run(state)

        LOGGER.info("Finished pipeline")
        return state
