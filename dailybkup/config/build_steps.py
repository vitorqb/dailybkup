from .common import ConfigBuildState, PConfigBuilder
from typing import TypeVar, Any
from .exceptions import MissingConfigKey
from .default import to_default, NO_DEFAULT


T = TypeVar("T", covariant=True)


class Required:
    def __init__(self, *attr_names: str):
        self._attr_names = attr_names

    def __call__(self, s: ConfigBuildState) -> None:
        for attr_name in self._attr_names:
            if attr_name in s.parsed:
                raise ValueError(f"Duplicated value for {attr_name}")
            if attr_name not in s.unparsed:
                raise MissingConfigKey(f"Missing key: {attr_name}")
            s.parsed[attr_name] = s.unparsed.pop(attr_name)


class Optional:
    def __init__(self, attr_name: str, default: Any):
        self._attr_name = attr_name
        self._default = to_default(default)

    def __call__(self, s: ConfigBuildState) -> None:
        if self._attr_name in s.parsed:
            raise ValueError(f"Duplicated value for {self._attr_name}")
        value = s.unparsed.pop(self._attr_name, self._default.value)
        if value is NO_DEFAULT:
            raise MissingConfigKey(f"Missing key: {self._attr_name}")
        s.parsed[self._attr_name] = value


class SubBuilder:
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
            raise ValueError(
                f"Can not builde because value for {self._attr_name} is not a dictionary"
            )
        s.parsed[self._attr_name] = self._builder.build(val)
