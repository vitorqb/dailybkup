import enum
import dataclasses
import datetime


@enum.unique
class Phase(enum.Enum):
    BEGIN = "BEGIN"
    COMPRESSION = "COMPRESSION"
    ENCRYPTION = "ENCRYPTION"
    STORAGE = "STORAGE"
    CLEANUP = "CLEANUP"
    NOTIFICATION = "NOTIFICATION"
    END = "END"


@dataclasses.dataclass
class PhaseTransitionLog:
    datetime_: datetime.datetime
    from_: Phase
    to_: Phase
