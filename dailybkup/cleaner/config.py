import dataclasses
from abc import ABC
import dailybkup.dictutils as dictutils
import dailybkup.config as configmod


class CleanerConfig(ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class B2CleanerConfig(CleanerConfig):
    retain_last: int
    bucket: str
    prefix: str = ""
    type_: str = "b2"


b2_cleaner_config_builder = dictutils.DictBuilder(
    ["bucket", "retain_last"],
    ["type_", "prefix"],
    B2CleanerConfig,
    missing_key_exception=configmod.MissingConfigKey,
    unknown_key_exception=configmod.UnkownConfigKey,
)
cleaner_config_builder: configmod.TypeDispatcherConfigBuilder[CleanerConfig]
cleaner_config_builder = configmod.TypeDispatcherConfigBuilder(
    {
        "b2": b2_cleaner_config_builder,
    }
)
