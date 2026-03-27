from dataclasses import dataclass
from .phases import Phase


@dataclass
class FrozenError:
    """
    Represents an error that happened at a specific state
    """

    source: Exception
    last_phase: Phase
