from .common import ConfigBuildState, PConfigBuilder
from typing import TypeVar
from .exceptions import MissingConfigKey


T = TypeVar("T", covariant=True)


class Required():
    def __init__(self, *attr_names: str):
        self._attr_names = attr_names

    def __call__(self, s: ConfigBuildState) -> None:
        for attr_name in self._attr_names:
            if attr_name in s.parsed:
                raise ValueError(f"Duplicated value for {attr_name}")
            if attr_name not in s.unparsed:
                raise MissingConfigKey(f"Missing key: {attr_name}")
            s.parsed[attr_name] = s.unparsed.pop(attr_name)


class SubBuilder():
    def __init__(self, attr_name: str, builder: PConfigBuilder[T]):
        self._attr_name = attr_name
        self._builder = builder

    def __call__(self, s: ConfigBuildState) -> None:
        if self._attr_name in s.parsed:
            raise ValueError(f"Duplicated value for {self._attr_name}")
        if self._attr_name not in s.unparsed:
            raise MissingConfigKey(f"Missing key: {self._attr_name}")
        val = s.unparsed.pop(self._attr_name)
        if not isinstance(val, dict):
            raise ValueError(f"Can not builde because value for {self._attr_name} is not a dictionary")
        s.parsed[self._attr_name] = self._builder.build(val)
