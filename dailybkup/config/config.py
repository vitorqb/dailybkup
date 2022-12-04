from typing import TypeVar, Dict, Protocol, Any, Generic
import copy
from .exceptions import MissingConfigKey


T = TypeVar("T", covariant=True)


class PConfigBuilder(Protocol[T]):
    def build(self, d: Dict[str, Any]) -> T:
        ...


class TypeDispatcherConfigBuilder(Generic[T]):
    def __init__(self, builders: Dict[str, PConfigBuilder]):
        self._builders = builders

    def build(self, d: Dict[str, Any]) -> T:
        dict_ = copy.deepcopy(d)
        type_ = dict_.pop("type_", "MISSING")
        if type_ == "MISSING":
            raise MissingConfigKey("Missing type_")
        builder = self._builders.get(type_)
        if builder is None:
            raise ValueError(f'Invalid type_ "{type_}"')
        return builder.build(dict_)
