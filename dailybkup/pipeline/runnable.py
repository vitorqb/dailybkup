from dailybkup import state as statemod

from typing import Protocol


class IRunnable(Protocol):
    def run(self, state: statemod.State) -> statemod.State:
        ...
