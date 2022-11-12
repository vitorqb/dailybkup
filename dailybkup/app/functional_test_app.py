"""
Functional tests for the app
"""
import dailybkup.tarutils as tarutils
import dailybkup.services.email_sender as email_sender
import pytest
import typer.testing
import dailybkup.app.cli as climod
import dailybkup.testutils as testutils
import dailybkup.gpgutils as gpgutils

import os
from dailybkup.testutils import p_
from dailybkup import injector


@pytest.fixture
def config_builder():
    return testutils.ConfigBuilder()


@pytest.fixture
def app():
    return climod.new_app()


@pytest.fixture
def cli_runner():
    return typer.testing.CliRunner()


@pytest.fixture
def b2_context():
    with testutils.b2_test_setup() as result:
        yield result


class TestFunctionalApp:
    def test_creates_tar_file(self, app, cli_runner, config_builder):
        config_builder.with_file_storage()
        with config_builder.build() as (config, config_file):
            result = cli_runner.invoke(app, ["-c", config_file, "backup"])
            assert result.exit_code == 0
            tar_file = config.storage[0].path
            assert os.path.exists(tar_file)
            assert p_("file1") in tarutils.list_files(tar_file)

    def test_encrypted_file(self, app, cli_runner, config_builder):
        config_builder.with_password_encryption("123456")
        config_builder.with_file_storage()
        with config_builder.build() as (config, config_file):
            result = cli_runner.invoke(app, ["-c", config_file, "backup"])
            assert result.exit_code == 0
            encrypted_file = config.storage[0].path
            with testutils.with_temp_file() as decrypted_file:
                gpgutils.decrypt(encrypted_file, "123456", decrypted_file)
                assert os.path.exists(decrypted_file)
                assert p_("file1") in tarutils.list_files(decrypted_file)

    def test_deletes_temporary_files(self, app, cli_runner, config_builder):
        config_builder.with_tempdir()
        config_builder.with_password_encryption()
        with config_builder.build() as (config, config_file):
            result = cli_runner.invoke(app, ["-c", config_file, "backup"])
            assert result.exit_code == 0
            assert os.path.isdir(config.tempdir)
            assert len(os.listdir(config.tempdir)) == 0

    def test_uploads_file_to_b2(self, app, cli_runner, b2_context, config_builder):
        config_builder.with_b2_storage(b2_context)
        with config_builder.build() as (config, config_file):
            result = cli_runner.invoke(app, ["-c", config_file, "backup"])
            assert result.exit_code == 0
            assert b2_context.count_files() == 1

    def test_runs_with_encryption_and_cleaner(
        self, app, cli_runner, b2_context, config_builder
    ):
        config_builder.with_password_encryption()
        config_builder.with_b2_storage(b2_context, ".tar.gz")
        config_builder.with_b2_cleaner(b2_context)
        with config_builder.build() as (config, config_file):
            result1 = cli_runner.invoke(app, ["-c", config_file, "backup"])
            assert result1.exit_code == 0
            injector.end()
            result2 = cli_runner.invoke(app, ["-c", config_file, "backup"])
            assert result2.exit_code == 0
            assert b2_context.count_files() == 1  # Cleaner cleaned 1 file
            assert list(b2_context.get_file_names())[0].endswith(".tar.gz")

    def test_notifies(self, app, cli_runner, config_builder):
        config_builder.with_mock_email_notifier()
        with config_builder.build() as (config, config_file):
            mock_sender_dir = config.notification[0].sender_config.directory
            mock_sender = email_sender.MockEmailSender(directory=mock_sender_dir)
            result = cli_runner.invoke(app, ["-c", config_file, "backup"])
            assert result.exit_code == 0
            assert mock_sender.count == 1
            assert mock_sender.last_email_petition.subject == "Backup completed!"
            assert mock_sender.last_email_petition.recipient_address == "foo@bar.baz"

    def test_notifies_failure(self, app, cli_runner, config_builder):
        config_builder.with_mock_email_notifier()
        config_builder.with_missconfigured_encryption()
        with config_builder.build() as (config, config_file):
            mock_sender_dir = config.notification[0].sender_config.directory
            mock_sender = email_sender.MockEmailSender(directory=mock_sender_dir)
            result1 = cli_runner.invoke(app, ["-c", config_file, "backup"])
            assert result1.exit_code == 1
            assert mock_sender.count == 1
            assert mock_sender.last_email_petition.subject == "Backup Failed!"
