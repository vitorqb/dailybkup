from typing import Dict, Any, Callable, Protocol, TypeVar
import dataclasses


LEGACYBuildStep = Callable[[Dict[str, Any]], Dict[str, Any]]
T = TypeVar("T", covariant=True)


class PConfigBuilder(Protocol[T]):
    def build(self, d: Dict[str, Any]) -> T:
        ...


@dataclasses.dataclass
class ConfigBuildState:
    unparsed: Dict[str, Any]
    parsed: Dict[str, Any]


BuildStep = Callable[[ConfigBuildState], None]
