from typing import Dict, Any, Callable, Protocol, TypeVar


BuildStep = Callable[[Dict[str, Any]], Dict[str, Any]]
T = TypeVar("T", covariant=True)


class PConfigBuilder(Protocol[T]):
    def build(self, d: Dict[str, Any]) -> T:
        ...
