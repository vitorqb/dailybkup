import pytest
from unittest import mock
from dailybkup.cleaner import config as configmod
from dailybkup import cleaner as sut
from dailybkup import state as statemod
from dailybkup.state import Phase

# This try-catch allows us to have tests both w/ and w/out optional
# gdrive dependencies
try:
    from dailybkup.gdrive_utils import GDriveFile
except ModuleNotFoundError:
    pass


def b2context_mock(*, file_names):
    b2context = mock.Mock()
    b2context.get_file_names.return_value = file_names
    return b2context


def gdrive_mock(*, files):
    gdrive = mock.Mock()
    gdrive.get_files.return_value = files
    return gdrive


class TestB2Cleaner:
    def test_calls_delete_on_single_old_file(self):
        b2context = b2context_mock(
            file_names=[
                "2020-01-01T12:00:00",
                "2020-01-02T12:00:00",
                "2020-01-03T12:00:00",
                "2020-01-04T12:00:00",
            ]
        )
        config = configmod.B2CleanerConfig(retain_last=3, bucket="foo")
        cleaner = sut.B2Cleaner(config, b2context=b2context)
        state = statemod.State.initial_state()

        cleaner.run(state)

        delete_calls = b2context.delete.call_args_list
        assert delete_calls == [
            mock.call("2020-01-01T12:00:00"),
        ]

    def test_calls_delete_on_old_files_many(self):
        b2context = b2context_mock(
            file_names=[
                "2020-01-01T12:00:00",
                "2020-01-02T12:00:00",
                "2020-01-03T12:00:00",
                "2020-01-04T12:00:00",
            ]
        )
        config = configmod.B2CleanerConfig(retain_last=2, bucket="foo")
        cleaner = sut.B2Cleaner(config, b2context=b2context)
        state = statemod.State.initial_state()

        cleaner.run(state)

        delete_calls = b2context.delete.call_args_list
        assert delete_calls == [
            mock.call("2020-01-01T12:00:00"),
            mock.call("2020-01-02T12:00:00"),
        ]

    def test_no_files_to_delete(self):
        b2context = b2context_mock(
            file_names=[
                "2020-01-01T12:00:00",
                "2020-01-04T12:00:00",
            ]
        )
        config = configmod.B2CleanerConfig(retain_last=2, bucket="foo")
        cleaner = sut.B2Cleaner(config, b2context=b2context)
        state = statemod.State.initial_state()

        cleaner.run(state)

        delete_calls = b2context.delete.call_args_list
        assert delete_calls == []


@pytest.mark.gdrive
class TestGDriveCleaner:
    def test_does_not_mutate_last_phase(self):
        client = gdrive_mock(files=[])
        config = configmod.GDriveCleanerConfig(retain_last=2, folder_id="foo")
        cleaner = sut.GDriveCleaner(config, client)
        state = statemod.State.initial_state()

        new_state = cleaner.run(state)

        assert new_state.last_phase == state.last_phase

    def test_cleans_2_files(self):
        client = gdrive_mock(
            files=[
                GDriveFile("2020-01-01T12:00:00", "1"),
                GDriveFile("2020-01-02T12:00:00", "2"),
                GDriveFile("2020-01-03T12:00:00", "3"),
                GDriveFile("2020-01-04T12:00:00", "4"),
            ]
        )
        config = configmod.GDriveCleanerConfig(retain_last=2, folder_id="foo")
        cleaner = sut.GDriveCleaner(config, client)
        state = statemod.State.initial_state()

        cleaner.run(state)

        client.delete_batch.assert_called_with(["1", "2"])

    def test_cleans_no_files(self):
        client = gdrive_mock(
            files=[
                GDriveFile("2020-01-01T12:00:00", "1"),
                GDriveFile("2020-01-02T12:00:00", "2"),
            ]
        )
        config = configmod.GDriveCleanerConfig(retain_last=2, folder_id="foo")
        cleaner = sut.GDriveCleaner(config, client)
        state = statemod.State.initial_state()

        cleaner.run(state)

        client.delete_batch.assert_called_with([])

    def test_cleans_no_files_because_of_prefix(self):
        client = gdrive_mock(
            files=[
                GDriveFile("2020-01-01T12:00:00", "1"),
                GDriveFile("2020-01-02T12:00:00", "2"),
                GDriveFile("2020-01-03T12:00:00", "3"),
                GDriveFile("2020-01-04T12:00:00", "4"),
            ]
        )
        config = configmod.GDriveCleanerConfig(
            retain_last=2, folder_id="foo", prefix="foo_"
        )
        cleaner = sut.GDriveCleaner(config, client)
        state = statemod.State.initial_state()

        cleaner.run(state)

        client.delete_batch.assert_called_with([])

    def test_cleans_2_files_with_prefix(self):
        client = gdrive_mock(
            files=[
                GDriveFile("foo_2020-01-01T12:00:00", "1"),
                GDriveFile("foo_2020-01-02T12:00:00", "2"),
                GDriveFile("foo_2020-01-03T12:00:00", "3"),
                GDriveFile("foo_2020-01-04T12:00:00", "4"),
                GDriveFile("bar_2020-01-01T12:00:00", "5"),
                GDriveFile("bar_2020-01-02T12:00:00", "6"),
            ]
        )
        config = configmod.GDriveCleanerConfig(
            retain_last=2, prefix="foo", folder_id="bar"
        )
        cleaner = sut.GDriveCleaner(config, client)
        state = statemod.State.initial_state()

        cleaner.run(state)

        client.delete_batch.assert_called_with(["1", "2"])


class TestNoOpCleaner:
    def test_does_not_sets_last_phase(self):
        state = statemod.State.initial_state()
        cleaner = sut.NoOpCleaner()

        new_state = cleaner.run(state)

        assert new_state.last_phase == state.last_phase
