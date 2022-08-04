import dataclasses
import dailybkup.testutils as testutils
import dailybkup.state as statemod
import dailybkup.config as configmod
import dailybkup.storer as sut
from dailybkup.phases import Phase


class TestFileStorer():
    def test_updates_state(self):
        with testutils.with_temp_file() as current_file:
            with testutils.with_temp_file() as dest_file:
                with open(current_file, 'wb') as f:
                    f.write(b'foo')
                config = configmod.FileStorageConfig(path=dest_file)
                state_1 = dataclasses.replace(
                    statemod.State.initial_state(),
                    current_file=current_file,
                )
                state_2 = sut.FileStorer(config).run(state_1)
                exp_state = dataclasses.replace(
                    state_1,
                    last_phase=Phase.STORAGE
                )
                assert state_2 == exp_state
