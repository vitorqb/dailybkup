import dataclasses
from typing import Sequence, List
import dailybkup.config as configmod


def DEFAULT_TAR_FLAGS():
    return ["--dereference", "--checkpoint=1000", "-v", "-z"]


@dataclasses.dataclass(frozen=True, kw_only=True)
class CompressionConfig:
    files: Sequence[str]
    exclude: Sequence[str]
    tar_executable: str = "tar"
    tar_flags: List[str] = dataclasses.field(default_factory=DEFAULT_TAR_FLAGS)


compression_config_builder = configmod.GenericBuilder(
    CompressionConfig,
    configmod.bs.Required("files", "exclude"),
    configmod.bs.Optional("tar_executable", "tar"),
    configmod.bs.Optional("tar_flags", DEFAULT_TAR_FLAGS()),
)
