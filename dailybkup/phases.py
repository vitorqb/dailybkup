import enum


@enum.unique
class Phase(enum.Enum):
    COMPRESSION: str = "COMPRESSION"
    ENCRYPTION: str = "ENCRYPTION"
    STORAGE: str = "STORAGE"
    CLEANUP: str = "CLEANUP"
    NOTIFICATION: str = "NOTIFICATION"
    END: str = "END"
