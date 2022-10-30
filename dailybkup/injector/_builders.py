from dailybkup import cleaner as cleanermod
from dailybkup import storer as storermod
from dailybkup import encryption as encryptionmod
from dailybkup import fileutils
import dailybkup.config as configmod
import dailybkup.b2utils as b2utils
from typing import Optional, Callable


class CleanerBuilder:
    def __init__(self, l_b2context: Callable[[str], b2utils.B2Context]):
        self._l_b2context = l_b2context

    def build(self, config: Optional[cleanermod.ICleanerConfig]) -> cleanermod.ICleaner:
        if config is None:
            return cleanermod.NoOpCleaner()
        if isinstance(config, cleanermod.B2CleanerConfig):
            b2context = self._l_b2context(config.bucket)
            return cleanermod.B2Cleaner(config, b2context=b2context)
        raise RuntimeError(f"Invalid config class {config.__class__}")


class StorerBuilder:
    def __init__(
        self,
        l_b2context: Callable[[str], b2utils.B2Context],
        l_backup_file_name_generator: Callable[
            [str], storermod.IBackupFileNameGenerator
        ],
    ):
        self._l_b2context = l_b2context
        self._l_backup_file_name_generator = l_backup_file_name_generator

    def build(self, config: storermod.IStorageConfig) -> storermod.IStorer:
        if isinstance(config, storermod.config.FileStorageConfig):
            return storermod.FileStorer(config)
        if isinstance(config, storermod.config.B2StorageConfig):
            b2context = self._l_b2context(config.bucket)
            backup_file_name_generator = self._l_backup_file_name_generator(
                config.suffix
            )
            return storermod.B2Storer(
                config,
                b2context,
                backup_file_name_generator=backup_file_name_generator,
            )
        raise RuntimeError(f"Uknown config class: {config}")


class EncryptorBuilder:
    def __init__(self, tempFileGenerator: fileutils.ITempFileGenerator):
        self._tempFileGenerator = tempFileGenerator

    def build(
        self, config: Optional[encryptionmod.IEncryptionConfig]
    ) -> encryptionmod.IEncryptor:
        if config is None:
            return encryptionmod.NoOpEncryptor()
        if isinstance(config, encryptionmod.PasswordEncryptionConfig):
            return encryptionmod.PasswordEncryptor(config, self._tempFileGenerator)
        raise ValueError(f"Unknown encryptor config: {config}")
