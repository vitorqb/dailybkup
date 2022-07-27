import copy
from abc import ABC
import dataclasses
from typing import Dict, Any, Sequence, ClassVar
import dailybkup.dictutils as dictutils


class UnkownConfigKey(RuntimeError):
    pass


class MissingConfigKey(RuntimeError):
    pass


#
# Config Protocols
#
class IDestinationConfig(ABC):
    pass


#
# Config classes
#
@dataclasses.dataclass(frozen=True, kw_only=True)
class Config():
    compressor: 'CompressorConfig'
    destination: Sequence['IDestinationConfig']


@dataclasses.dataclass(frozen=True, kw_only=True)
class CompressorConfig():
    files: Sequence[str]
    exclude: Sequence[str]
    tar_executable: str = "tar"


@dataclasses.dataclass(frozen=True, kw_only=True)
class FileDestinationConfig(IDestinationConfig):
    path: str
    type_: str = "file"
    _req_fields: ClassVar[Sequence[str]] = ['path']
    _opt_fields: ClassVar[Sequence[str]] = ['type_']


#
# Builder classes
#
class ConfigDictBuilder(dictutils.PDictBuilder[Config]):
    def build(cls, d: Dict[str, Any]) -> 'Config':
        missing_keys = {'compressor', 'destination'} - {x for x in d.keys()}
        if missing_keys:
            raise MissingConfigKey(f'Missing configuration keys:  {missing_keys}')
        compressor = compressor_config_builder.build(d['compressor'])
        destination = [destination_config_builder.build(x) for x in d['destination']]
        return Config(compressor=compressor, destination=destination)


class DestinationConfigBuilder(dictutils.PDictBuilder[IDestinationConfig]):

    def build(cls, d: Dict[str, Any]) -> IDestinationConfig:
        dict_ = copy.deepcopy(d)
        type_ = dict_.pop('type_', 'MISSING')
        if type_ == 'file':
            return file_destination_config_builder.build(d)
        elif type_ == 'MISSING':
            raise MissingConfigKey('Missing key type_ for destination config')
        else:
            raise ValueError(f'Invalid type_ "{type_}" for destination config')


#
# Builder instances
#
config_builder = ConfigDictBuilder()
compressor_config_builder: dictutils.DictBuilder = dictutils.DictBuilder(
    cls_=CompressorConfig,
    req_fields=['files', 'exclude'],
    opt_fields=['tar_executable'],
    missing_key_exception=MissingConfigKey,
    unknown_key_exception=UnkownConfigKey,
)
destination_config_builder = DestinationConfigBuilder()
file_destination_config_builder = dictutils.DictBuilder(
    ['path'],
    ['type_'],
    FileDestinationConfig,
    missing_key_exception=MissingConfigKey,
    unknown_key_exception=UnkownConfigKey,
)


#
# Dumper instances
#
dumper: dictutils.DictDumper = dictutils.DictDumper()
