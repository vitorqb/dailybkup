import datetime
from dailybkup import storer
from dailybkup import testutils
from dailybkup import cleaner as sut
from dailybkup import state as statemod
from dailybkup.phases import Phase
from dailybkup import config as configmod


def fake_now_1():
    return datetime.datetime(2020, 1, 1)


def fake_now_2():
    return datetime.datetime(2020, 1, 3)


def fake_now_3():
    return datetime.datetime(2020, 1, 5)


name_generator_1 = storer.BackupFileNameGenerator(suffix="", now_fn=fake_now_1)
name_generator_2 = storer.BackupFileNameGenerator(suffix="", now_fn=fake_now_2)
name_generator_3 = storer.BackupFileNameGenerator(suffix="", now_fn=fake_now_3)


class TestFunctionalB2Cleaner:
    def test_cleans_old_files(self):
        with testutils.b2_test_setup() as b2context:
            b2context.create_empty_file(name_generator_1.generate())
            b2context.create_empty_file(name_generator_2.generate())
            b2context.create_empty_file(name_generator_3.generate())
            assert b2context.count_files() == 3
            state = statemod.State.initial_state()
            config = configmod.B2CleanerConfig(retain_last=1, bucket="foo")

            new_state = sut.B2Cleaner(config, b2context=b2context).run(state)

            assert list(b2context.get_file_names()) == [name_generator_3.generate()]
            assert new_state.last_phase == Phase.CLEANUP
