import dataclasses
from dailybkup import state as statemod
from dailybkup.phases import Phase


class Finisher:
    def should_run(self, state: statemod.State) -> bool:
        return True

    def run(self, state: statemod.State) -> statemod.State:
        return dataclasses.replace(state, last_phase=Phase.END)
