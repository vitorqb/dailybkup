import datetime
import dataclasses
from dailybkup import encryption as sut
from dailybkup import state as statemod
from dailybkup.testutils import p
import dailybkup.state.mutations as m
from dailybkup.encryption import config as configmod
from dailybkup.state import Phase
import dailybkup.fileutils as fileutils
import dailybkup.testutils as testutils
import os


class TestPasswordEncryptor:
    def test_encrypts_tar_file(self):
        config = configmod.PasswordEncryptionConfig(password="foo")
        state = statemod.State(current_file=p("file1"))
        encryptor = sut.PasswordEncryptor(config, fileutils.TempFileGenerator())
        newstate = encryptor.run(state)
        assert os.path.exists(newstate.encrypted_file)
        # not should modify last_phase
        assert newstate.last_phase == state.last_phase
        assert newstate.current_file == newstate.encrypted_file


class TestNoOpEncryptor:
    def test_updates_phase(self):
        with testutils.mock_now(datetime.datetime(2022, 1, 1)):
            state_1 = statemod.State.initial_state()
            state_2 = sut.NoOpEncryptor().run(state_1)
            assert state_2 == state_1
