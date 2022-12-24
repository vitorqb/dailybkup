from abc import ABC
import dataclasses
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


file_storage_config_builder: configmod.PConfigBuilder[FileStorageConfig]
file_storage_config_builder = configmod.GenericBuilder(
    FileStorageConfig,
    configmod.bs.Required("path"),
    configmod.bs.Optional("type_", "file"),
)
b2_storage_config_builder: configmod.PConfigBuilder[B2StorageConfig]
b2_storage_config_builder = configmod.GenericBuilder(
    B2StorageConfig,
    configmod.bs.Required("bucket", "suffix"),
    configmod.bs.Optional("type_", "b2"),
    configmod.bs.Optional("prefix", ""),
)
storage_config_builder: configmod.TypeDispatcherConfigBuilder[IStorageConfig]
storage_config_builder = configmod.TypeDispatcherConfigBuilder(
    {
        "file": file_storage_config_builder,
        "b2": b2_storage_config_builder,
    }
)
