from typing import Dict, Any, Callable, Protocol, TypeVar
import dataclasses


T = TypeVar("T", covariant=True)


class PConfigBuilder(Protocol[T]):
    def build(self, d: Dict[str, Any]) -> T:
        ...


@dataclasses.dataclass
class ConfigBuildState:
    unparsed: Dict[str, Any]
    parsed: Dict[str, Any]


BuildStep = Callable[[ConfigBuildState], None]
