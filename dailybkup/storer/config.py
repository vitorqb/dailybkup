import copy
from abc import ABC
import dataclasses
import dailybkup.dictutils as dictutils
import dailybkup.config.exceptions as config_exceptions
from typing import Dict, Any


class IStorageConfig(ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class FileStorageConfig(IStorageConfig):
    path: str
    type_: str = "file"


@dataclasses.dataclass(frozen=True, kw_only=True)
class B2StorageConfig(IStorageConfig):
    bucket: str
    suffix: str
    prefix: str = ""
    type_: str = "b2"


class StorageConfigBuilder(dictutils.PDictBuilder[IStorageConfig]):
    def build(cls, d: Dict[str, Any]) -> IStorageConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.pop("type_", "MISSING")
        if type_ == "file":
            return file_storage_config_builder.build(dict_)
        elif type_ == "b2":
            return b2_storage_config_builder.build(dict_)
        elif type_ == "MISSING":
            raise config_exceptions.MissingConfigKey(
                "Missing key type_ for storage config"
            )
        else:
            raise ValueError(f'Invalid type_ "{type_}" for storage config')


file_storage_config_builder = dictutils.DictBuilder(
    ["path"],
    ["type_"],
    FileStorageConfig,
    missing_key_exception=config_exceptions.MissingConfigKey,
    unknown_key_exception=config_exceptions.UnkownConfigKey,
)
b2_storage_config_builder = dictutils.DictBuilder(
    ["bucket", "suffix"],
    ["type_", "prefix"],
    B2StorageConfig,
    missing_key_exception=config_exceptions.MissingConfigKey,
    unknown_key_exception=config_exceptions.UnkownConfigKey,
)
storage_config_builder = StorageConfigBuilder()
