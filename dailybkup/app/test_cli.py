import dailybkup.app.cli as sut
import dailybkup.injector
import dailybkup.state as statemod
import dailybkup.state.mutations as m
import unittest.mock as mock
import pytest
import typer.testing
import re


semver_regexp = re.compile("^([0-9]+)\\.([0-9]+)\\.([0-9]+)$")


@pytest.fixture
def app():
    return sut.new_app()


@pytest.fixture
def cli_runner():
    return typer.testing.CliRunner()


@pytest.fixture
def injector():
    injector = mock.Mock()
    injector.pipeline_runner().run.return_value = statemod.State.initial_state()
    with mock.patch("dailybkup.injector.get") as get:
        get.return_value = injector
        yield injector


class TestApp:
    def test_run_command_dispatches_to_runner(self, injector, cli_runner, app):
        result = cli_runner.invoke(app, "backup")
        assert result.exit_code == 0
        injector.pipeline_runner().run.assert_called_with(injector.initial_state())

    def test_run_version_prints_version(self, cli_runner, app):
        result = cli_runner.invoke(app, "version")
        assert result.exit_code == 0
        assert semver_regexp.match(result.stdout.strip())

    @pytest.mark.parametrize(
        "phase",
        [
            statemod.Phase.BEGIN,
            statemod.Phase.COMPRESSION,
            statemod.Phase.ENCRYPTION,
            statemod.Phase.STORAGE,
        ],
    )
    def test_backup_raises_error_on_phases(self, phase, injector, cli_runner, app):
        # Arrange
        err = RuntimeError("foo")
        state = statemod.State().mutate(m.with_last_phase(phase), m.with_error(err))
        pipeline_runner = mock.Mock()
        pipeline_runner.run.return_value = state
        injector.pipeline_runner.return_value = pipeline_runner

        # Action
        result = cli_runner.invoke(app, "backup")

        # Assert
        assert result.exit_code == 1
        assert "foo" in result.output

    @pytest.mark.parametrize(
        "phase",
        [
            statemod.Phase.CLEANUP,
            statemod.Phase.NOTIFICATION,
            statemod.Phase.END,
        ],
    )
    def test_backup_does_not_raises_error_on_phases(
        self, phase, injector, cli_runner, app
    ):
        # Arrange
        err = RuntimeError("foo")
        state = statemod.State().mutate(m.with_last_phase(phase), m.with_error(err))
        pipeline_runner = mock.Mock()
        pipeline_runner.run.return_value = state
        injector.pipeline_runner.return_value = pipeline_runner

        # Action
        result = cli_runner.invoke(app, "backup")

        # Assert
        assert result.exit_code == 0
        assert "foo" in result.output
