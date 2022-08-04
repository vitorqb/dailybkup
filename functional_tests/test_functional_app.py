"""
Functional tests for the app
"""
import dailybkup.tarutils as tarutils
import pytest
import typer.testing
import dailybkup.app as appmod
import dailybkup.config as configmod
import dailybkup.testutils as testutils
import dailybkup.gpgutils as gpgutils
import dataclasses
import os
import dailybkup.injector as injector
from dailybkup.testutils import p, p_


# TODO - Those features are repeated from dailybkup/conftest.py
# how an we unify them?
@pytest.fixture(autouse=True)
def injector_cleanup():
    """
    Ensures we clean up the global setup in the `injector` module.
    """
    try:
        yield
    finally:
        injector.end()


@pytest.fixture
def app():
    return appmod.new_app()


@pytest.fixture
def cli_runner():
    return typer.testing.CliRunner()


@pytest.fixture
def config1():
    with testutils.with_temp_file() as storage_file:
        return configmod.config_builder.build({
            "compression": {
                "files": [p("file1"), p("dir1")],
                "exclude": [],
            },
            "storage": [
                {
                    "type_": "file",
                    "path": storage_file
                }
            ]
        })


class TestFunctionalApp():

    def test_creates_tar_file(self, app, cli_runner, config1):
        with testutils.config_to_file(config1) as config1_file:
            result = cli_runner.invoke(app, ['-c', config1_file, 'backup'])
            assert result.exit_code == 0
            tar_file = config1.storage[0].path
            assert os.path.exists(tar_file)
            assert p_("file1") in tarutils.list_files(tar_file)

    def test_encrypted_file(self, app, cli_runner, config1):
        config1 = dataclasses.replace(config1, encryption={
            "type_": "password",
            "password": "123456",
        })
        with testutils.config_to_file(config1) as config1_file:
            result = cli_runner.invoke(app, ['-c', config1_file, 'backup'])
            assert result.exit_code == 0
            encrypted_file = config1.storage[0].path
            with testutils.with_temp_file() as decrypted_file:
                gpgutils.decrypt(encrypted_file, "123456", decrypted_file)
                assert os.path.exists(decrypted_file)
                assert p_("file1") in tarutils.list_files(decrypted_file)
