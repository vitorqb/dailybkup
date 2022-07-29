import copy
from abc import ABC
import dataclasses
from typing import Dict, Any, Sequence, ClassVar
import dailybkup.dictutils as dictutils


#
# Exceptions
#
class UnkownConfigKey(RuntimeError):
    pass


class MissingConfigKey(RuntimeError):
    pass


#
# Config Protocols
#
class IStorageConfig(ABC):
    pass


#
# Config classes
#
@dataclasses.dataclass(frozen=True, kw_only=True)
class Config():
    compression: 'CompressionConfig'
    storage: Sequence['IStorageConfig']


@dataclasses.dataclass(frozen=True, kw_only=True)
class CompressionConfig():
    files: Sequence[str]
    exclude: Sequence[str]
    tar_executable: str = "tar"


@dataclasses.dataclass(frozen=True, kw_only=True)
class FileStorageConfig(IStorageConfig):
    path: str
    type_: str = "file"
    _req_fields: ClassVar[Sequence[str]] = ['path']
    _opt_fields: ClassVar[Sequence[str]] = ['type_']


#
# Builder classes
#
class ConfigDictBuilder(dictutils.PDictBuilder[Config]):
    def build(cls, d: Dict[str, Any]) -> 'Config':
        missing_keys = {'compression', 'storage'} - {x for x in d.keys()}
        if missing_keys:
            raise MissingConfigKey(f'Missing configuration keys:  {missing_keys}')
        compression = compression_config_builder.build(d['compression'])
        storage = [storage_config_builder.build(x) for x in d['storage']]
        return Config(compression=compression, storage=storage)


class StorageConfigBuilder(dictutils.PDictBuilder[IStorageConfig]):

    def build(cls, d: Dict[str, Any]) -> IStorageConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.pop('type_', 'MISSING')
        if type_ == 'file':
            return file_storage_config_builder.build(d)
        elif type_ == 'MISSING':
            raise MissingConfigKey('Missing key type_ for storage config')
        else:
            raise ValueError(f'Invalid type_ "{type_}" for storage config')


#
# Builder instances
#
config_builder = ConfigDictBuilder()
compression_config_builder: dictutils.DictBuilder = dictutils.DictBuilder(
    cls_=CompressionConfig,
    req_fields=['files', 'exclude'],
    opt_fields=['tar_executable'],
    missing_key_exception=MissingConfigKey,
    unknown_key_exception=UnkownConfigKey,
)
storage_config_builder = StorageConfigBuilder()
file_storage_config_builder = dictutils.DictBuilder(
    ['path'],
    ['type_'],
    FileStorageConfig,
    missing_key_exception=MissingConfigKey,
    unknown_key_exception=UnkownConfigKey,
)


#
# Dumper instances
#
dumper: dictutils.DictDumper = dictutils.DictDumper()
