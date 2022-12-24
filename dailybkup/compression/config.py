import dataclasses
from typing import Sequence
import dailybkup.config as configmod


@dataclasses.dataclass(frozen=True, kw_only=True)
class CompressionConfig:
    files: Sequence[str]
    exclude: Sequence[str]
    tar_executable: str = "tar"


compression_config_builder = configmod.GenericBuilder(
    CompressionConfig,
    configmod.bs.Required("files", "exclude"),
    configmod.bs.Optional("tar_executable", "tar"),
)
