import dataclasses
from dailybkup.phases import Phase
from typing import List, Optional


@dataclasses.dataclass(frozen=True, kw_only=True)
class State():
    last_phase: Optional[Phase] = None
    files: Optional[List[str]] = None
    compression_logfile: Optional[str] = None
    compressed_file: Optional[str] = None

    @classmethod
    def initial_state(cls) -> 'State':
        return cls()
