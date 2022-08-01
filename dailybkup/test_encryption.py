from dailybkup import encryption as sut
from dailybkup import state as statemod
from dailybkup.testutils import p
from dailybkup import config as configmod
from dailybkup.phases import Phase
import os


class TestPasswordEncryptor():
    def test_encrypts_tar_file(self):
        config = configmod.PasswordEncryptionConfig(password="foo")
        state = statemod.State(compressed_file=p("file1"))
        encryptor = sut.PasswordEncryptor(config)
        newstate = encryptor.run(state)
        assert os.path.exists(newstate.encrypted_file)
        assert newstate.last_phase == Phase.ENCRYPTION
