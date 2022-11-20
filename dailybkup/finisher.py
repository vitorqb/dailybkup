import dataclasses
from dailybkup import state as statemod
import dailybkup.state.mutations as m
from dailybkup.phases import Phase


class Finisher:
    def should_run(self, state: statemod.State) -> bool:
        return True

    def run(self, state: statemod.State) -> statemod.State:
        return state.mutate(m.with_last_phase(Phase.END))
