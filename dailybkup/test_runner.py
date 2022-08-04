from unittest import mock
import dailybkup.runner as sut
import dailybkup.state as state
import dailybkup.compression as compression
import dailybkup.encryption as encryption
from dailybkup.phases import Phase


class TestRunner():

    def test_run(self):
        compressor = compression.MockCompressor(mock.Mock())
        storers = []
        encryptor = encryption.NoOpEncryptor()
        result = sut.Runner(
            compressor=compressor,
            storers=storers,
            encryptor=encryptor,
        ).run()
        initial_state = state.State.initial_state()
        final_state = state.State(last_phase=Phase.ENCRYPTION, files=["foo"])
        assert compressor.calls == [initial_state]
        assert result == final_state
