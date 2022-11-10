import os
import shutil
import dataclasses
import dailybkup.app as app
import dailybkup.compression as compressionmod
import dailybkup.encryption as encryptionmod
import dailybkup.storer as storermod
import dailybkup.cleaner as cleanermod
import dailybkup.fileutils as fileutils
import dailybkup.b2utils as b2utils
import dailybkup.services.email_sender as email_sender
import dailybkup.notifier as notifiermod
import contextlib
from typing import Iterator, Tuple
from .testutils import p, config_to_file


def default_config() -> app.config.Config:
    return app.config.Config(
        compression=compressionmod.CompressionConfig(
            files=[p("file1"), p("dir1")],
            exclude=[],
        ),
        encryption=None,
        storage=[],
        cleaner=[],
        notification=[],
        tempdir=None,
    )


class _LazyTempFileController:
    def __init__(self):
        self._filenames = []
        self._dirnames = []

    def new(self) -> str:
        filename = fileutils.TempFileGenerator().gen_name()
        self._filenames.append(filename)
        return filename

    def new_dir(self) -> str:
        dirname = fileutils.TempFileGenerator().gen_name()
        self._dirnames.append(dirname)
        return dirname

    def create(self):
        for dirname in self._dirnames:
            os.mkdir(dirname)

    def clean_all(self):
        for filename in self._filenames:
            try:
                os.remove(filename)
            except FileNotFoundError:
                pass
        for dirname in self._dirnames:
            shutil.rmtree(dirname)


class ConfigBuilder:
    def __init__(self, config=None):
        self._config = config or default_config()
        self._tempfile_controller = _LazyTempFileController()

    def with_password_encryption(self, password: str = "foo") -> None:
        encryption_config = encryptionmod.PasswordEncryptionConfig(password=password)
        self.replace(encryption=encryption_config)

    def with_file_storage(self, path=None) -> None:
        path = path or self._tempfile_controller.new()
        storage_config = storermod.FileStorageConfig(path=path)
        self.replace(storage=[*self._config.storage, storage_config])

    def with_b2_storage(
        self, b2context: b2utils.B2Context, suffix: str = ".tar"
    ) -> None:
        storage_config = storermod.B2StorageConfig(
            bucket=b2context.bucket_name,
            suffix=suffix,
            prefix=b2context.prefix,
        )
        self.replace(storage=[*self._config.storage, storage_config])

    def with_b2_cleaner(
        self,
        b2context: b2utils.B2Context,
        retain_last: int = 1,
    ) -> None:
        cleaner_config = cleanermod.B2CleanerConfig(
            retain_last=retain_last,
            bucket=b2context.bucket_name,
            prefix=b2context.prefix,
        )
        self.replace(cleaner=[*self._config.cleaner, cleaner_config])

    def with_mock_email_notifier(
        self,
        directory=None,
        recipient_address="foo@bar.baz",
    ) -> None:
        directory = directory or self._tempfile_controller.new_dir()
        sender_config = email_sender.MockEmailSenderConfig(directory=directory)
        notification_config = notifiermod.EmailNotifierConfig(
            recipient_address=recipient_address,
            sender_config=sender_config,
        )
        self.replace(notification=[*self._config.notification, notification_config])

    def with_tempdir(self, tempdir=None) -> None:
        self.replace(tempdir=self._tempfile_controller.new_dir())

    def replace(self, **changes) -> None:
        self._config = dataclasses.replace(self._config, **changes)

    @contextlib.contextmanager
    def build(self) -> Iterator[Tuple[app.config.Config, str]]:
        assert self._config
        self._tempfile_controller.create()
        with config_to_file(self._config) as config_file:
            try:
                yield (self._config, config_file)
            finally:
                self._tempfile_controller.clean_all()
