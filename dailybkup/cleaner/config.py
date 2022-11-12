import dataclasses
import copy
from abc import ABC
import dailybkup.dictutils as dictutils
from typing import Dict, Any
import dailybkup.config as configmod


class CleanerConfig(ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class B2CleanerConfig(CleanerConfig):
    retain_last: int
    bucket: str
    prefix: str = ""
    type_: str = "b2"


class CleanerConfigBuilder(dictutils.PDictBuilder[CleanerConfig]):
    def build(self, d: Dict[str, Any]) -> CleanerConfig:
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
    ["type_", "prefix"],
    B2CleanerConfig,
    missing_key_exception=configmod.exceptions.MissingConfigKey,
    unknown_key_exception=configmod.exceptions.UnkownConfigKey,
)
