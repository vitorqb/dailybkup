"""
Functional tests for the app
"""
import dailybkup.tarutils as tarutils
import dailybkup.services.email_sender as email_sender
import pytest
import typer.testing
import dailybkup.app.cli as climod
import dailybkup.app as appmod
import dailybkup.testutils as testutils
import dailybkup.gpgutils as gpgutils
import dailybkup.storer as storermod
import dailybkup.notifier as notifiermod

import dataclasses
import os
import tempfile
from dailybkup.testutils import p, p_
from dailybkup import injector


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


@pytest.fixture
def config2():
    with testutils.with_temp_file() as storage_file:
        return appmod.config.config_builder.build(
            {
                "compression": {
                    "files": [p("file1"), p("dir1")],
                    "exclude": [],
                },
                "storage": [{"type_": "file", "path": storage_file}],
            }
        )


@pytest.fixture
def config3(b2_context):
    with testutils.with_temp_file() as storage_file:
        return appmod.config.config_builder.build(
            {
                "compression": {
                    "files": [p("file1"), p("dir1")],
                    "exclude": [],
                },
                "encryption": {
                    "type_": "password",
                    "password": "pass",
                },
                "storage": [
                    {
                        "type_": "b2",
                        "suffix": ".tar.gz",
                        "bucket": b2_context.bucket_name,
                        "prefix": b2_context.prefix,
                    }
                ],
                "cleaner": [
                    {
                        "type_": "b2",
                        "retain_last": 1,
                        "bucket": b2_context.bucket_name,
                        "prefix": b2_context.prefix,
                    }
                ],
            }
        )


class TestFunctionalApp:
    def test_creates_tar_file(self, app, cli_runner, config2):
        with testutils.config_to_file(config2) as config2_file:
            result = cli_runner.invoke(app, ["-c", config2_file, "backup"])
            assert result.exit_code == 0
            tar_file = config2.storage[0].path
            assert os.path.exists(tar_file)
            assert p_("file1") in tarutils.list_files(tar_file)

    def test_encrypted_file(self, app, cli_runner, config2):
        config2 = dataclasses.replace(
            config2,
            encryption={
                "type_": "password",
                "password": "123456",
            },
        )
        with testutils.config_to_file(config2) as config2_file:
            result = cli_runner.invoke(app, ["-c", config2_file, "backup"])
            assert result.exit_code == 0
            encrypted_file = config2.storage[0].path
            with testutils.with_temp_file() as decrypted_file:
                gpgutils.decrypt(encrypted_file, "123456", decrypted_file)
                assert os.path.exists(decrypted_file)
                assert p_("file1") in tarutils.list_files(decrypted_file)

    def test_deletes_temporary_files(self, app, cli_runner, config2):
        with tempfile.TemporaryDirectory() as tempdir:
            config2 = dataclasses.replace(
                config2,
                tempdir=tempdir,
                # Adds encryption so more tempfiles to remove
                encryption={"type_": "password", "password": "123456"},
            )
            with testutils.config_to_file(config2) as config2_file:
                result = cli_runner.invoke(app, ["-c", config2_file, "backup"])
                assert result.exit_code == 0
                assert os.path.isdir(tempdir)
                assert len(os.listdir(tempdir)) == 0

    def test_uploads_file_to_b2(self, app, cli_runner, config2, b2_context):
        b2_storage_config = storermod.config.B2StorageConfig(
            bucket=b2_context.bucket_name,
            suffix=".tar",
            prefix=b2_context.prefix,
        )
        config2 = dataclasses.replace(config2, storage=[b2_storage_config])
        with testutils.config_to_file(config2) as config2_file:
            result = cli_runner.invoke(app, ["-c", config2_file, "backup"])
            assert result.exit_code == 0
            assert b2_context.count_files() == 1

    def test_runs_with_encryption_and_cleaner(
        self, app, cli_runner, b2_context, config3
    ):
        with testutils.config_to_file(config3) as config3_file:
            result1 = cli_runner.invoke(app, ["-c", config3_file, "backup"])
            assert result1.exit_code == 0
            injector.end()
            result2 = cli_runner.invoke(app, ["-c", config3_file, "backup"])
            assert result2.exit_code == 0
            assert b2_context.count_files() == 1  # Cleaner cleaned 1 file
            assert list(b2_context.get_file_names())[0].endswith(".tar.gz")

    def test_notifies(self, app, cli_runner, config2):
        with testutils.with_temp_dir() as temp_dir:
            sender_config = email_sender.MockEmailSenderConfig(directory=temp_dir)
            notification_config = [
                notifiermod.EmailNotifierConfig(
                    recipient_address="foo@bar.baz",
                    sender_config=sender_config,
                )
            ]
            mock_sender = email_sender.MockEmailSender(directory=temp_dir)
            config2 = dataclasses.replace(config2, notification=notification_config)
            with testutils.config_to_file(config2) as config2_file:
                result = cli_runner.invoke(app, ["-c", config2_file, "backup"])
                assert result.exit_code == 0
                assert mock_sender.count == 1
                assert mock_sender.last_email_petition.subject == "Backup completed!"
                assert (
                    mock_sender.last_email_petition.recipient_address == "foo@bar.baz"
                )
