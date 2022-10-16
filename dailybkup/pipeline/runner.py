from dailybkup import state as statemod
import logging


from typing import Sequence
from .runnable import IRunnable


LOGGER = logging.getLogger(__name__)


class Runner(IRunnable):

    def __init__(self, *, steps: Sequence[IRunnable], hooks: Sequence[statemod.IPhaseTransitionHook]):
        self._steps = steps
        self._hooks = hooks

    def run(self, state: statemod.State) -> statemod.State:
        LOGGER.info("Starting pipeline")
        old_state = None
        new_state = state
        for step in self._steps:
            LOGGER.info("Running pipeline step: %s", step)
            old_state = new_state
            new_state = step.run(old_state)
            new_state = self._run_hooks(old_state, new_state)
        LOGGER.info("Pipeline finished")
        return new_state

    def _run_hooks(self, old_state: statemod.State, new_state: statemod.State) -> statemod.State:
        final_state = new_state
        for hook in self._hooks:
            if hook.should_run(old_state, new_state):
                final_state = hook.run(final_state)
        return final_state
