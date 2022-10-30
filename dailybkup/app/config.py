import dataclasses
from typing import Dict, Any, Sequence, Optional
import dailybkup.dictutils as dictutils
import dailybkup.config.exceptions as exceptions
import dailybkup.storer.config as storer_config
import dailybkup.encryption as encryptionmod
import dailybkup.cleaner as cleanermod
import dailybkup.compression as compressionmod


#
# Config classes
#
@dataclasses.dataclass(frozen=True, kw_only=True)
class Config:
    compression: compressionmod.CompressionConfig
    encryption: Optional[encryptionmod.IEncryptionConfig] = None
    storage: Sequence[storer_config.IStorageConfig]
    cleaner: Sequence[cleanermod.ICleanerConfig] = dataclasses.field(
        default_factory=list
    )
    tempdir: Optional[str] = None


#
# Builder classes
#
class ConfigDictBuilder(dictutils.PDictBuilder[Config]):
    def build(cls, d: Dict[str, Any]) -> "Config":
        missing_keys = {"compression", "storage"} - {x for x in d.keys()}
        if missing_keys:
            raise exceptions.MissingConfigKey(
                f"Missing configuration keys:  {missing_keys}"
            )
        kwargs = dict(
            compression=compressionmod.config.compression_config_builder.build(
                d["compression"]
            ),
            storage=[
                storer_config.storage_config_builder.build(x) for x in d["storage"]
            ],
            tempdir=d.get("tempdir"),
        )
        if d.get("encryption") is not None:
            kwargs["encryption"] = encryptionmod.encryption_config_builder.build(
                d["encryption"]
            )
        cleaner_configs = d.get("cleaner")
        if cleaner_configs is not None:
            kwargs["cleaner"] = [
                cleanermod.config.cleaner_config_builder.build(x)
                for x in cleaner_configs
            ]
        return Config(**kwargs)


#
# Builder instances
#
config_builder = ConfigDictBuilder()


#
# Dumper instances
#
dumper: dictutils.DictDumper = dictutils.DictDumper()
