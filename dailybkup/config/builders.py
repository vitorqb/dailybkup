from typing import Generic, TypeVar, Dict, Any
from .common import PConfigBuilder
from .exceptions import MissingConfigKey


T = TypeVar("T", covariant=True)


class SubBuilder(Generic[T]):
    def __init__(self, attr_name: str, builder: PConfigBuilder[T]):
        self._attr_name = attr_name
        self._builder = builder

    def __call__(self, d: Dict[str, Any]) -> Dict[str, Any]:
        sub_dict = d.pop(self._attr_name, None)
        if sub_dict is None:
            raise MissingConfigKey(f"Missing key {self._attr_name}")
        d[self._attr_name] = self._builder.build(sub_dict)
        return d


class Required:
    def __init__(self, attr_name: str):
        self._attr_name = attr_name

    def __call__(self, d: Dict[str, Any]) -> Dict[str, Any]:
        if self._attr_name not in d:
            raise MissingConfigKey(f"Missing key {self._attr_name}")
        return d
