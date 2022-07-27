import dailybkup.state as statemod
import dailybkup.compression as compression
import dailybkup.destinator as destinatormod
from typing import Sequence


class Runner():
    """
    Class responsible to run all phases of the backup.
    """

    def __init__(
            self,
            *,
            compressor: compression.ICompressor,
            destinators: Sequence[destinatormod.IDestinator],
    ):
        self._compressor: compression.ICompressor = compressor
        self._destinators: Sequence[destinatormod.IDestinator] = destinators

    def run(self) -> statemod.State:
        state = statemod.State.initial_state()
        state = self._compressor.run(state)
        for destinator in self._destinators:
            state = destinator.run(state)
        return state
