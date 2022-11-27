import pytest
import dataclasses

from unittest import mock

from dailybkup import state as statemod
from dailybkup.pipeline import runner as sut
from dailybkup.state import Phase
import dailybkup.state.mutations as m


@pytest.fixture
def logger_mock():
    with mock.patch("dailybkup.pipeline.runner.LOGGER") as mock_logger:
        yield mock_logger


class MockCompressionTransitionHook(statemod.IPhaseTransitionHook):
    def __init__(self):
        self.calls = []

    def should_run(self, old_state: statemod.State, new_state: statemod.State) -> bool:
        return new_state.last_phase == Phase.COMPRESSION

    def run(self, state: statemod.State) -> statemod.State:
        self.calls.append(state)
        return state.mutate(m.with_compressed_file("bar"))


class MockCompressionStep:
    def should_run(self, state: statemod.State) -> bool:
        return state.error is None

    def run(self, state: statemod.State) -> statemod.State:
        return state.mutate(m.with_last_phase(Phase.COMPRESSION))


class TestRunner:
    def test_zero_steps(self):
        # ARRANGE
        initial_state = statemod.State.initial_state()
        steps = []
        hooks = []
        runner = sut.Runner(steps=steps, hooks=hooks)

        # ACT
        result = runner.run(initial_state)

        # ASSERT
        assert result == initial_state

    def test_two_steps(self):
        # ARRANGE
        initial_state = statemod.State.initial_state()
        steps = [mock.Mock(), mock.Mock()]
        hooks = []
        runner = sut.Runner(steps=steps, hooks=hooks)

        # ACT
        result = runner.run(initial_state)

        # ASSERT
        assert result == steps[1].run.return_value
        steps[0].run.assert_called_with(initial_state)

    def test_calls_loggers(self, logger_mock):
        # ARRANGE
        initial_state = statemod.State.initial_state()
        steps = [mock.Mock()]
        hooks = []
        runner = sut.Runner(steps=steps, hooks=hooks)

        # ACT
        runner.run(initial_state)

        # ASSERT
        info_calls = logger_mock.info.call_args_list
        assert info_calls[0][0] == ("Starting pipeline",)
        assert info_calls[1][0] == ("Running pipeline step: %s", steps[0])
        assert info_calls[2][0] == ("Pipeline finished",)

    def test_run_hooks(self):
        # ARRANGE
        initial_state = statemod.State.initial_state()
        steps = [MockCompressionStep()]
        hooks = [MockCompressionTransitionHook()]
        runner = sut.Runner(steps=steps, hooks=hooks)

        # ACT
        final_state = runner.run(initial_state)

        # ARRANGE
        assert len(hooks[0].calls) == 1
        assert hooks[0].calls[0].last_phase == Phase.COMPRESSION
        final_state.compressed_file == "bar"

    def test_does_run_hook_if_hook_should_not_run(self):
        # ARRANGE
        initial_state = statemod.State.initial_state()
        steps = [mock.Mock()]
        hooks = [MockCompressionTransitionHook()]
        runner = sut.Runner(steps=steps, hooks=hooks)

        # ACT
        runner.run(initial_state)

        # ARRANGE
        assert hooks[0].calls == []

    def test_sets_error_on_error(self):
        # ARRANGE
        initial_state = statemod.State.initial_state()
        error = RuntimeError("FOO")
        steps = [mock.Mock()]
        steps[0].run.side_effect = error
        hooks = []
        runner = sut.Runner(steps=steps, hooks=hooks)

        # ACT
        final_state = runner.run(initial_state)

        # ARRANGE
        final_state.error == error

    def test_only_runs_if_should_run_is_true(self):
        # ARRANGE
        initial_state = statemod.State.initial_state()
        steps = [mock.Mock()]
        steps[0].should_run.return_value = False
        hooks = []
        runner = sut.Runner(steps=steps, hooks=hooks)

        # ACT
        final_state = runner.run(initial_state)

        # ARRANGE
        assert steps[0].run.call_args is None
        assert final_state is initial_state
