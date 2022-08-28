from unittest import mock
import dailybkup.runner as sut
import dailybkup.storer as storermod
import dailybkup.state as state
import dailybkup.compression as compression
import dailybkup.encryption as encryption
from dailybkup.phases import Phase


class TestRunner():

    def test_run(self):
        compressor = compression.MockCompressor(mock.Mock(), mock.Mock())
        storer = storermod.CompositeStorer([])
        encryptor = encryption.NoOpEncryptor()
        result = sut.Runner(
            compressor=compressor,
            storer=storer,
            encryptor=encryptor,
        ).run()
        initial_state = state.State.initial_state()
        final_state = state.State(last_phase=Phase.END, files=["foo"])
        assert compressor.calls == [initial_state]
        assert result == final_state

    def test_run_phase_transition_hooks(self):
        phase_transition_hooks = [
            state.MockPhaseTransitionHook(should_run=True),
            state.MockPhaseTransitionHook(should_run=False),
        ]
        compressor = compression.MockCompressor(mock.Mock(), mock.Mock())
        storer = storermod.CompositeStorer([])
        encryptor = encryption.NoOpEncryptor()
        runner = sut.Runner(
            compressor=compressor,
            storer=storer,
            encryptor=encryptor,
            phase_transition_hooks=phase_transition_hooks
        )
        final_state = runner.run()
        assert phase_transition_hooks[0].call_count == 4
        assert phase_transition_hooks[0].last_state == final_state
        assert phase_transition_hooks[1].call_count == 0
        assert phase_transition_hooks[1].last_state is None
