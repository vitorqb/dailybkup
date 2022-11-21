import enum
import dataclasses
import datetime


@enum.unique
class Phase(enum.Enum):
    BEGIN: str = "BEGIN"
    COMPRESSION: str = "COMPRESSION"
    ENCRYPTION: str = "ENCRYPTION"
    STORAGE: str = "STORAGE"
    CLEANUP: str = "CLEANUP"
    NOTIFICATION: str = "NOTIFICATION"
    END: str = "END"


@dataclasses.dataclass
class PhaseTransitionLog:
    datetime_: datetime.datetime
    from_: Phase
    to_: Phase
