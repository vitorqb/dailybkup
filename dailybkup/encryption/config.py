import dataclasses
from abc import ABC
import dailybkup.config as configmod


class IEncryptionConfig(ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class PasswordEncryptionConfig(IEncryptionConfig):
    type_: str = "password"
    password: str


password_encryption_config_builder = configmod.GenericBuilder(
    PasswordEncryptionConfig,
    configmod.bs.Required("password"),
)
encryption_config_builder: configmod.TypeDispatcherConfigBuilder[IEncryptionConfig]
encryption_config_builder = configmod.TypeDispatcherConfigBuilder(
    {"password": password_encryption_config_builder}
)
