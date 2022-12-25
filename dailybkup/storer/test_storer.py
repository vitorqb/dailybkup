from datetime import datetime
import dailybkup.testutils as testutils
import dailybkup.state as statemod
import dailybkup.storer.config as configmod
import dailybkup.storer as sut
import dailybkup.state.mutations as m
import dailybkup.fileutils as fileutils
from dailybkup.state import Phase
import unittest.mock as mock


def fake_now():
    return datetime(2011, 12, 2)


class TestBackupFileNameGenerator:
    def test_generate_based_on_current_datetime(self):
        generator = sut.BackupFileNameGenerator(suffix=".tar.gz", now_fn=fake_now)
        assert generator.generate() == "2011-12-02T00:00:00.tar.gz"


class TestFileStorer:
    def test_updates_state(self):
        with (
            testutils.with_temp_file() as current_file,
            testutils.with_temp_dir() as dest_directory,
            testutils.with_temp_file() as dest_file,
            testutils.mock_now(datetime(2021, 12, 31)),
        ):
            file_name_generator = sut.BackupFileNameGenerator(
                suffix=".tar.gz", now_fn=fake_now
            )
            fileutils.write_str(current_file, "foo")
            config = configmod.FileStorageConfig(
                LEGACYpath=dest_file, directory=dest_directory
            )
            state_1 = statemod.State.initial_state().mutate(
                m.with_current_file(current_file)
            )
            state_2 = sut.FileStorer(
                config, backup_file_name_generator=file_name_generator
            ).run(state_1)
            exp_state = state_1.mutate(m.with_last_phase(Phase.STORAGE))
            assert state_2 == exp_state
            assert (
                fileutils.read_as_str(
                    f"{dest_directory}/{file_name_generator.generate()}"
                )
                == "foo"
            )


class TestCompositeStorer:
    def test_calls_all_storers(self):
        # ARRANGE
        state = statemod.State.initial_state(current_file="/")
        storers = [mock.Mock(), mock.Mock()]
        for storer in storers:
            storer.run.return_value = state
        storer = sut.CompositeStorer(storers)

        # ACT
        final_state = storer.run(state)

        # ASSERT
        for storer in storers:
            storer.run.assert_called_once_with(state)
        assert final_state.last_phase == Phase.STORAGE
        assert final_state.current_file is None
