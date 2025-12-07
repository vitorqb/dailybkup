from dailybkup import state as statemod

from typing import Protocol


class PRunnable(Protocol):
    def should_run(self, state: statemod.State) -> bool: ...

    def run(self, state: statemod.State) -> statemod.State: ...

    def get_phase(self) -> statemod.Phase: ...
