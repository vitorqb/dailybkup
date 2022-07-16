import dailybkup.state as statemod
import dailybkup.compression as compression


class Runner():
    """
    Class responsible to run all phases of the backup.
    """

    def __init__(self, *, compressor: compression.ICompressor):
        self._compressor: compression.ICompressor = compressor

    def run(self) -> statemod.State:
        state = statemod.State.initial_state()
        print(state)
        state = self._compressor.run(state)
        print(state)
        return state
