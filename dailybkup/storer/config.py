from abc import ABC
import dataclasses
import dailybkup.dictutils as dictutils
import dailybkup.config as configmod


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


file_storage_config_builder = dictutils.DictBuilder(
    ["path"],
    ["type_"],
    FileStorageConfig,
    missing_key_exception=configmod.MissingConfigKey,
    unknown_key_exception=configmod.UnkownConfigKey,
)
b2_storage_config_builder = dictutils.DictBuilder(
    ["bucket", "suffix"],
    ["type_", "prefix"],
    B2StorageConfig,
    missing_key_exception=configmod.MissingConfigKey,
    unknown_key_exception=configmod.UnkownConfigKey,
)
storage_config_builder: configmod.TypeDispatcherConfigBuilder[IStorageConfig]
storage_config_builder = configmod.TypeDispatcherConfigBuilder(
    {
        "file": file_storage_config_builder,
        "b2": b2_storage_config_builder,
    }
)
