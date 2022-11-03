import dataclasses
import abc


class IEmailSenderConfig(abc.ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class MockEmailSenderConfig(IEmailSenderConfig):
    type_: str = "mock"
    directory: str
