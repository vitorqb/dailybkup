import dataclasses
from typing import List, Optional
import dailybkup.timeutils as timeutils
from .phases import Phase, PhaseTransitionLog
from .state import StateMutation, State


def with_last_phase(last_phase: Phase) -> StateMutation:
    def inner_with_last_phase(state: State):
        phase_transition_logs = [
            *state.phase_transition_logs,
            PhaseTransitionLog(timeutils.now(), state.last_phase, last_phase),
        ]
        return dataclasses.replace(
            state, last_phase=last_phase, phase_transition_logs=phase_transition_logs
        )

    return inner_with_last_phase


def with_files(files: List[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, files=files)


def with_compression_logfile(compression_logfile: Optional[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, compression_logfile=compression_logfile)


def with_compressed_file(compressed_file: Optional[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, compressed_file=compressed_file)


def with_encrypted_file(encrypted_file: Optional[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, encrypted_file=encrypted_file)


def with_current_file(current_file: Optional[str]) -> StateMutation:
    return lambda x: dataclasses.replace(x, current_file=current_file)


def with_error(error: Optional[Exception]) -> StateMutation:
    return lambda x: dataclasses.replace(x, error=error)
