from dailybkup.storer.storer import (
    IStorer,
    IBackupFileNameGenerator,
    FileStorer,
    B2Storer,
)
from dailybkup.storer.config import IStorageConfig, FileStorageConfig, B2StorageConfig
import dailybkup.b2utils as b2utils
from typing import Callable


class StorerBuilder:
    def __init__(
        self,
        l_b2context: Callable[[str], b2utils.B2Context],
        l_backup_file_name_generator: Callable[[str], IBackupFileNameGenerator],
    ):
        self._l_b2context = l_b2context
        self._l_backup_file_name_generator = l_backup_file_name_generator

    def build(self, config: IStorageConfig) -> IStorer:
        if isinstance(config, FileStorageConfig):
            return FileStorer(config)
        if isinstance(config, B2StorageConfig):
            b2context = self._l_b2context(config.bucket)
            backup_file_name_generator = self._l_backup_file_name_generator(
                config.suffix
            )
            return B2Storer(
                config,
                b2context,
                backup_file_name_generator=backup_file_name_generator,
            )
        raise RuntimeError(f"Uknown config class: {config}")
