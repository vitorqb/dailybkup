import dataclasses
from abc import ABC
import dailybkup.config as configmod


class CleanerConfig(ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class B2CleanerConfig(CleanerConfig):
    retain_last: int
    bucket: str
    prefix: str = ""
    type_: str = "b2"


@dataclasses.dataclass(frozen=True, kw_only=True)
class GDriveCleanerConfig(CleanerConfig):
    retain_last: int
    folder_id: str
    prefix: str = ""
    type_: str = "google-drive"


b2_cleaner_config_builder = configmod.GenericBuilder(
    B2CleanerConfig,
    configmod.bs.Required("bucket", "retain_last"),
    configmod.bs.Optional("type_", "b2"),
    configmod.bs.Optional("prefix", ""),
)
gdrive_config_builder = configmod.GenericBuilder(
    GDriveCleanerConfig,
    configmod.bs.Required("retain_last", "folder_id"),
    configmod.bs.Optional("type_", "google-drive"),
    configmod.bs.Optional("prefix", ""),
)
cleaner_config_builder: configmod.TypeDispatcherConfigBuilder[CleanerConfig]
cleaner_config_builder = configmod.TypeDispatcherConfigBuilder(
    {
        "b2": b2_cleaner_config_builder,
        "google-drive": gdrive_config_builder,
    }
)
