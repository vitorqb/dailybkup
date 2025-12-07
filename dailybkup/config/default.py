from typing_extensions import runtime_checkable, Protocol
from typing import Any, Optional
import dailybkup.envutils as envutils


NO_DEFAULT = object()


@runtime_checkable
class PDefaultValue(Protocol):
    @property
    def value(self) -> Any: ...


class StaticDefaultValue:
    def __init__(self, value: Any):
        self.value = value


class DefaultFromEnv:
    def __init__(self, env_var_name: str):
        self._env_var_name = env_var_name

    @property
    def value(self) -> Optional[str]:
        return envutils.get(self._env_var_name, NO_DEFAULT)


def static(x: Any) -> PDefaultValue:
    return StaticDefaultValue(x)


def env(x: str) -> PDefaultValue:
    return DefaultFromEnv(x)


def to_default(x: Any) -> PDefaultValue:
    if isinstance(x, PDefaultValue):
        return x
    return StaticDefaultValue(x)
