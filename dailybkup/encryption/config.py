import dataclasses
from abc import ABC
import dailybkup.dictutils as dictutils
from typing import Dict, Any
import copy
import dailybkup.config.exceptions as config_exceptions


class IEncryptionConfig(ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class PasswordEncryptionConfig(IEncryptionConfig):
    type_: str = "password"
    password: str


class EncryptionConfigBuilder(dictutils.PDictBuilder[IEncryptionConfig]):
    def build(self, d: Dict[str, Any]) -> IEncryptionConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.pop("type_", "MISSING")
        if type_ == "password":
            return password_encryption_config_builder.build(dict_)
        elif type_ == "MISSING":
            raise config_exceptions.MissingConfigKey(
                "Missing key type_ for storage config"
            )
        else:
            raise ValueError(f'Invalid type_ "{type_}" for storage config')


encryption_config_builder = EncryptionConfigBuilder()
password_encryption_config_builder = dictutils.DictBuilder(
    ["password"],
    [],
    PasswordEncryptionConfig,
    missing_key_exception=config_exceptions.MissingConfigKey,
    unknown_key_exception=config_exceptions.UnkownConfigKey,
)
