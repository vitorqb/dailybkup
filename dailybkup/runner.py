import dailybkup.state as statemod
import dailybkup.compression as compression
import dailybkup.storer as storermod
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
    ):
        self._compressor: compression.ICompressor = compressor
        self._storers: Sequence[storermod.IStorer] = storers

    def run(self) -> statemod.State:
        state = statemod.State.initial_state()

        LOGGER.info("Running compression")
        state = self._compressor.run(state)

        LOGGER.info("Running storers")
        for storer in self._storers:
            state = storer.run(state)

        LOGGER.info("Finished pipeline")
        return state
