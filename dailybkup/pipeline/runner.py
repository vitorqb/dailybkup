from dailybkup import state as statemod
import logging


from typing import Sequence
from .runnable import PRunnable


LOGGER = logging.getLogger(__name__)


class Runner:
    def __init__(
        self,
        *,
        steps: Sequence[PRunnable],
        hooks: Sequence[statemod.IPhaseTransitionHook]
    ):
        self._steps = steps
        self._hooks = hooks

    def run(self, state: statemod.State) -> statemod.State:
        LOGGER.info("Starting pipeline")
        old_state = None
        new_state = state
        for step in self._steps:
            if step.should_run(new_state):
                LOGGER.info("Running pipeline step: %s", step)
                old_state = new_state
                try:
                    new_state = step.run(old_state)
                except Exception as e:
                    LOGGER.error("Catched exception: %s", e)
                    new_state = old_state.with_error(e)
                new_state = self._run_hooks(old_state, new_state)
            else:
                LOGGER.info("Skipping pipeline step: %s", step)
        LOGGER.info("Pipeline finished")
        return new_state

    def _run_hooks(
        self, old_state: statemod.State, new_state: statemod.State
    ) -> statemod.State:
        final_state = new_state
        for hook in self._hooks:
            if hook.should_run(old_state, new_state):
                final_state = hook.run(final_state)
        return final_state
