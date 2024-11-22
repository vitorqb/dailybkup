from dailybkup import state as statemod
import dailybkup.state.mutations as m
from dailybkup.state import Phase


class Finisher:
    def should_run(self, state: statemod.State) -> bool:
        return True

    def get_phase(self) -> Phase:
        return Phase.END

    def run(self, state: statemod.State) -> statemod.State:
        return state
