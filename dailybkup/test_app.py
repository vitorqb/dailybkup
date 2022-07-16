import dailybkup.app as sut
import pytest
import typer.testing
import re


semver_regexp = re.compile("^([0-9]+)\\.([0-9]+)\\.([0-9]+)$")


@pytest.fixture
def app():
    return sut.new_app()


@pytest.fixture
def runner():
    return typer.testing.CliRunner()


class TestApp():

    def test_run_command_dispatches_to_runner(self, runner, app):
        result = runner.invoke(app, 'backup')
        assert result.exit_code != 0

    def test_run_version_prints_version(self, runner, app):
        result = runner.invoke(app, 'version')
        assert result.exit_code == 0
        assert semver_regexp.match(result.stdout.strip())
