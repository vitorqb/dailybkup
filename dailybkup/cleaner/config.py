import dataclasses
import copy
from abc import ABC
import dailybkup.dictutils as dictutils
from typing import Dict, Any
import dailybkup.config as configmod


class ICleanerConfig(ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class B2CleanerConfig(ICleanerConfig):
    retain_last: int
    bucket: str
    type_: str = "b2"


class CleanerConfigBuilder(dictutils.PDictBuilder[ICleanerConfig]):
    def build(self, d: Dict[str, Any]) -> ICleanerConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.pop("type_", "MISSING")
        if type_ == "b2":
            return b2_cleaner_config_builder.build(dict_)
        if type_ == "MISSING":
            raise configmod.exceptions.MissingConfigKey(
                "Missing key type_ for cleaner config"
            )
        raise ValueError(f'Invalid type_ "{type_}" for cleaner config')


cleaner_config_builder = CleanerConfigBuilder()
b2_cleaner_config_builder = dictutils.DictBuilder(
    ["bucket", "retain_last"],
    ["type_"],
    B2CleanerConfig,
    missing_key_exception=configmod.exceptions.MissingConfigKey,
    unknown_key_exception=configmod.exceptions.UnkownConfigKey,
)
