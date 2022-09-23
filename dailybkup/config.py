import copy
from abc import ABC
import dataclasses
from typing import Dict, Any, Sequence, ClassVar, Optional
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


class IEncryptionConfig(ABC):
    pass


class ICleanerConfig(ABC):
    pass


#
# Config classes
#
@dataclasses.dataclass(frozen=True, kw_only=True)
class Config():
    compression: 'CompressionConfig'
    encryption: Optional[IEncryptionConfig] = None
    storage: Sequence['IStorageConfig']
    tempdir: Optional[str] = None


@dataclasses.dataclass(frozen=True, kw_only=True)
class CompressionConfig():
    files: Sequence[str]
    exclude: Sequence[str]
    tar_executable: str = "tar"


@dataclasses.dataclass(frozen=True, kw_only=True)
class FileStorageConfig(IStorageConfig):
    path: str
    type_: str = "file"


@dataclasses.dataclass(frozen=True, kw_only=True)
class B2StorageConfig(IStorageConfig):
    bucket: str
    suffix: str
    type_: str = "b2"


@dataclasses.dataclass(frozen=True, kw_only=True)
class B2CleanerConfig(ICleanerConfig):
    retain_last: int


@dataclasses.dataclass(frozen=True, kw_only=True)
class PasswordEncryptionConfig(IEncryptionConfig):
    type_: str = "password"
    password: str


#
# Builder classes
#
class ConfigDictBuilder(dictutils.PDictBuilder[Config]):
    def build(cls, d: Dict[str, Any]) -> 'Config':
        missing_keys = {'compression', 'storage'} - {x for x in d.keys()}
        if missing_keys:
            raise MissingConfigKey(f'Missing configuration keys:  {missing_keys}')
        kwargs = dict(
            compression=compression_config_builder.build(d['compression']),
            storage=[storage_config_builder.build(x) for x in d['storage']],
            tempdir=d.get('tempdir'),
        )
        if d.get('encryption') is not None:
            kwargs['encryption'] = encryption_config_builder.build(d['encryption'])
        return Config(**kwargs)


class StorageConfigBuilder(dictutils.PDictBuilder[IStorageConfig]):
    def build(cls, d: Dict[str, Any]) -> IStorageConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.pop('type_', 'MISSING')
        if type_ == 'file':
            return file_storage_config_builder.build(dict_)
        elif type_ == 'b2':
            return b2_storage_config_builder.build(dict_)
        elif type_ == 'MISSING':
            raise MissingConfigKey('Missing key type_ for storage config')
        else:
            raise ValueError(f'Invalid type_ "{type_}" for storage config')


class EncryptionConfigBuilder(dictutils.PDictBuilder[IEncryptionConfig]):
    def build(self, d: Dict[str, Any]) -> IEncryptionConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.pop('type_', 'MISSING')
        if type_ == 'password':
            return password_encryption_config_builder.build(dict_)
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
encryption_config_builder = EncryptionConfigBuilder()
password_encryption_config_builder = dictutils.DictBuilder(
    ['password'],
    [],
    PasswordEncryptionConfig,
    missing_key_exception=MissingConfigKey,
    unknown_key_exception=UnkownConfigKey,
)
file_storage_config_builder = dictutils.DictBuilder(
    ['path'],
    ['type_'],
    FileStorageConfig,
    missing_key_exception=MissingConfigKey,
    unknown_key_exception=UnkownConfigKey,
)
b2_storage_config_builder = dictutils.DictBuilder(
    ['bucket', 'suffix'],
    ['type_'],
    B2StorageConfig,
    missing_key_exception=MissingConfigKey,
    unknown_key_exception=UnkownConfigKey,
)


#
# Dumper instances
#
dumper: dictutils.DictDumper = dictutils.DictDumper()
