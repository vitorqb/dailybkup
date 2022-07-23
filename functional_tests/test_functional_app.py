"""
Functional tests for the app
"""
import contextlib
import pytest
import yaml
import typer.testing
import dailybkup.app as appmod
import dailybkup.config as configmod
import dailybkup.testutils as testutils
from dailybkup.testutils import p


@pytest.fixture
def app():
    return appmod.new_app()


@pytest.fixture
def cli_runner():
    return typer.testing.CliRunner()


@pytest.fixture
def temp_file():
    with testutils.with_temp_file() as f:
        yield f


@pytest.fixture
def config1():
    return configmod.Config.from_dict({
        "compressor": {
            "files": [p("file1"), p("dir1")],
            "exclude": [],
        }
    })


class TestFunctionalApp():

    def test_creates_tar_file(self, app, cli_runner, config1):
        with testutils.config_to_file(config1) as config1_file:
            result = cli_runner.invoke(app, ['-c', config1_file, 'backup'])
            assert result.exit_code == 0
