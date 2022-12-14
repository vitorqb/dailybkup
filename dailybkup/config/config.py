from typing import TypeVar, Dict, Any, Generic, Callable
import copy
from .exceptions import MissingConfigKey
from .common import BuildStep, PConfigBuilder


T = TypeVar("T", covariant=True)


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


class GenericBuilder(Generic[T]):
    def __init__(self, constructor: Callable[..., T], *steps: BuildStep):
        self._constructor = constructor
        self._steps = steps

    def build(self, d: Dict[str, Any]) -> T:
        out = copy.deepcopy(d)
        for step in self._steps:
            out = step(out)
        return self._constructor(**out)
