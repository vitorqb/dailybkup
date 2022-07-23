import copy
import dataclasses
from typing import Dict, Any, List


class UnkownConfigKey(RuntimeError):
    pass


class MissingConfigKey(RuntimeError):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class Config():

    compressor: 'CompressorConfig'

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Config':
        compressor = CompressorConfig.from_dict(d['compressor'])
        return cls(compressor=compressor)

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass(frozen=True, kw_only=True)
class CompressorConfig():
    files: List[str]
    exclude: List[str]
    tar_executable: str = "tar"

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'CompressorConfig':
        req_fields = ['files', 'exclude']
        opt_fields = ['tar_executable']
        fields = [*req_fields, *opt_fields]
        d = copy.deepcopy(d)
        kwargs = {}
        for k in fields:
            if k in d:
                kwargs[k] = d.pop(k)
        if len(d.keys()) > 0:
            raise UnkownConfigKey(f"Unexpected key {k} for {cls}")
        missing_keys = [k for k in req_fields if k not in kwargs]
        if missing_keys:
            raise MissingConfigKey(f"Key(s) is/are missing: {missing_keys}")
        return cls(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)
