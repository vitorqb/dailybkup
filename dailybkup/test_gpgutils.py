import pytest
from dailybkup import testutils
from dailybkup.testutils import p, p_
from dailybkup import gpgutils as sut
import filecmp
import os


class TestGpgUtils:
    def test_encrypt_and_decrypt_file(self):
        infile = p("file1")
        with testutils.with_temp_file() as encrypted_file:
            sut.encrypt(infile, "abc123def", encrypted_file)
            assert os.path.exists(encrypted_file)
            with testutils.with_temp_file() as decrypted_file:
                sut.decrypt(encrypted_file, "abc123def", decrypted_file)
                assert filecmp.cmp(infile, decrypted_file)

    def test_fails_with_empty_passphrase(self):
        infile = p("file1")
        with testutils.with_temp_file() as encrypted_file:
            with pytest.raises(sut.GPGExecutionFailed):
                sut.encrypt(infile, "", encrypted_file)

    def test_fails_with_infile_not_exist(self):
        infile = p("DONOTEXIST")
        with testutils.with_temp_file() as encrypted_file:
            with pytest.raises(sut.GPGExecutionFailed):
                sut.encrypt(infile, "abc123def", encrypted_file)
