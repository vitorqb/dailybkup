import datetime
import dailybkup.state as statemod
import dailybkup.state.mutations as m
import dailybkup.testutils as testutils
from .phases import Phase, PhaseTransitionLog


class TestMutations:
    def test_mutations(self):
        initial_state = statemod.State.initial_state()
        an_error = RuntimeError("FOO")
        final_state = initial_state.mutate(
            m.with_last_phase(Phase.END),
            m.with_files(["foo"]),
            m.with_compression_logfile("bar"),
            m.with_compressed_file("baz"),
            m.with_encrypted_file("boz"),
            m.with_current_file("buz"),
            m.with_error(an_error),
        )
        assert final_state.last_phase == Phase.END
        assert final_state.files == ["foo"]
        assert final_state.compression_logfile == "bar"
        assert final_state.compressed_file == "baz"
        assert final_state.encrypted_file == "boz"
        assert final_state.current_file == "buz"
        assert final_state.error == an_error

    def test_mutating_last_phase_creates_record(self):
        with testutils.mock_now(datetime.datetime(222, 1, 1)) as now:
            initial_state = statemod.State.initial_state()
            final_state = initial_state.mutate(m.with_last_phase(Phase.COMPRESSION))
            assert final_state.phase_transition_logs == [
                PhaseTransitionLog(now(), Phase.BEGIN, Phase.COMPRESSION)
            ]
