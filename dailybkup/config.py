import copy
from abc import ABC
import dataclasses
from typing import Dict, Any, Sequence, Protocol, TypeVar, Generic, Type, ClassVar
import dailybkup.dictutils as dictutils


class UnkownConfigKey(RuntimeError):
    pass


class MissingConfigKey(RuntimeError):
    pass


class PDictBuildable(Protocol):
    _req_fields: Sequence[str]
    _opt_fields: Sequence[str]


T = TypeVar('T', bound=PDictBuildable)


class ConfigDictBuilderMixin(Generic[T]):
    @classmethod
    def from_dict(cls: Type[T], dict_: Dict[str, Any]) -> T:
        req_fields = cls._req_fields
        opt_fields = cls._opt_fields
        builder = dictutils.DictBuilder(req_fields, opt_fields, cls)
        try:
            return builder.build(dict_)
        except dictutils.MissingKey as e:
            raise MissingConfigKey(str(e))
        except dictutils.UnkownKey as e:
            raise UnkownConfigKey(str(e))


class DictDumpableMixin():
    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Config(DictDumpableMixin):

    compressor: 'CompressorConfig'
    destination: Sequence['IDestinationConfig']

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Config':
        missing_keys = {'compressor', 'destination'} - {x for x in d.keys()}
        if missing_keys:
            raise MissingConfigKey(f'Missing configuration keys:  {missing_keys}')
        compressor = CompressorConfig.from_dict(d['compressor'])
        destination = [build_destination_config(x) for x in d['destination']]
        return cls(compressor=compressor, destination=destination)


@dataclasses.dataclass(frozen=True, kw_only=True)
class CompressorConfig(ConfigDictBuilderMixin, DictDumpableMixin):
    files: Sequence[str]
    exclude: Sequence[str]
    tar_executable: str = "tar"

    _req_fields: ClassVar[Sequence[str]] = ['files', 'exclude']
    _opt_fields: ClassVar[Sequence[str]] = ['tar_executable']


class IDestinationConfig(ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class FileDestinationConfig(IDestinationConfig, ConfigDictBuilderMixin, DictDumpableMixin):
    path: str
    type_: str = "file"
    _req_fields: ClassVar[Sequence[str]] = ['path']
    _opt_fields: ClassVar[Sequence[str]] = ['type_']


def build_destination_config(dict_: Dict[str, Any]) -> IDestinationConfig:
    dict_ = copy.deepcopy(dict_)
    type_ = dict_.pop('type_', 'MISSING')
    if type_ == 'file':
        return FileDestinationConfig.from_dict(dict_)
    elif type_ == 'MISSING':
        raise MissingConfigKey('Missing key type_ for destination config')
    else:
        raise ValueError(f'Invalid type_ "{type_}" for destination config')
