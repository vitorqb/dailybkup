from .encryption import IEncryptor, NoOpEncryptor, PasswordEncryptor
from .config import IEncryptionConfig, PasswordEncryptionConfig
from dailybkup import fileutils
from typing import Optional


class EncryptorBuilder:
    def __init__(self, tempFileGenerator: fileutils.ITempFileGenerator):
        self._tempFileGenerator = tempFileGenerator

    def build(self, config: Optional[IEncryptionConfig]) -> IEncryptor:
        if config is None:
            return NoOpEncryptor()
        if isinstance(config, PasswordEncryptionConfig):
            return PasswordEncryptor(config, self._tempFileGenerator)
        raise ValueError(f"Unknown encryptor config: {config}")
