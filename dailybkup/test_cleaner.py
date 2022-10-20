import pytest

from unittest import mock
from dailybkup import config as configmod
from dailybkup import cleaner as sut
from dailybkup import state as statemod
from dailybkup.phases import Phase


def b2context_mock(*, file_names):
    b2context = mock.Mock()
    b2context.get_file_names.return_value = file_names
    return b2context


class TestB2Cleaner():

    def test_calls_delete_on_single_old_file(self):
        b2context = b2context_mock(file_names=[
            "2020-01-01T12:00:00",
            "2020-01-02T12:00:00",
            "2020-01-03T12:00:00",
            "2020-01-04T12:00:00",
        ])
        config = configmod.B2CleanerConfig(retain_last=3, bucket="foo")
        cleaner = sut.B2Cleaner(config, b2context=b2context)
        state = statemod.State.initial_state()

        cleaner.run(state)

        delete_calls = b2context.delete.call_args_list
        assert delete_calls == [
            mock.call("2020-01-01T12:00:00"),
        ]

    def test_calls_delete_on_old_files_many(self):
        b2context = b2context_mock(file_names=[
            "2020-01-01T12:00:00",
            "2020-01-02T12:00:00",
            "2020-01-03T12:00:00",
            "2020-01-04T12:00:00",
        ])
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
        b2context = b2context_mock(file_names=[
            "2020-01-01T12:00:00",
            "2020-01-04T12:00:00",
        ])
        config = configmod.B2CleanerConfig(retain_last=2, bucket="foo")
        cleaner = sut.B2Cleaner(config, b2context=b2context)
        state = statemod.State.initial_state()

        cleaner.run(state)

        delete_calls = b2context.delete.call_args_list
        assert delete_calls == []


class TestNoOpCleaner():

    def test_sets_last_phase(self):
        state = statemod.State.initial_state()
        cleaner = sut.NoOpCleaner()

        new_state = cleaner.run(state)

        assert new_state.last_phase == Phase.CLEANUP
