import dataclasses
from typing import Sequence
import dailybkup.dictutils as dictutils
import dailybkup.config.exceptions as config_exceptions


@dataclasses.dataclass(frozen=True, kw_only=True)
class CompressionConfig:
    files: Sequence[str]
    exclude: Sequence[str]
    tar_executable: str = "tar"


compression_config_builder: dictutils.DictBuilder = dictutils.DictBuilder(
    cls_=CompressionConfig,
    req_fields=["files", "exclude"],
    opt_fields=["tar_executable"],
    missing_key_exception=config_exceptions.MissingConfigKey,
    unknown_key_exception=config_exceptions.UnkownConfigKey,
)
