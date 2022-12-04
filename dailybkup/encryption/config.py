import dataclasses
from abc import ABC
import dailybkup.dictutils as dictutils
from typing import Dict, Any
import copy
import dailybkup.config as configmod


class IEncryptionConfig(ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class PasswordEncryptionConfig(IEncryptionConfig):
    type_: str = "password"
    password: str


password_encryption_config_builder = dictutils.DictBuilder(
    ["password"],
    [],
    PasswordEncryptionConfig,
    missing_key_exception=configmod.MissingConfigKey,
    unknown_key_exception=configmod.UnkownConfigKey,
)
encryption_config_builder: configmod.TypeDispatcherConfigBuilder[IEncryptionConfig]
encryption_config_builder = configmod.TypeDispatcherConfigBuilder(
    {"password": password_encryption_config_builder}
)
