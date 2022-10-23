import dailybkup.app as sut
import dailybkup.injector
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
