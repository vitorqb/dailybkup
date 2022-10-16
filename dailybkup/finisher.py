import dataclasses
from dailybkup import state as statemod
from dailybkup.pipeline import IRunnable
from dailybkup.phases import Phase


class Finisher(IRunnable):

    def run(self, state: statemod.State) -> statemod.State:
        return dataclasses.replace(state, last_phase=Phase.END)
