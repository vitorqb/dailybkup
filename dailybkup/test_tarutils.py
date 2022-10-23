import dailybkup.tarutils as sut
import pytest
import subprocess
from dailybkup.testutils import p, p_
import dailybkup.testutils as testutils


@pytest.fixture
def logfile():
    with testutils.with_temp_file() as f:
        yield f


@pytest.fixture
def destfile():
    with testutils.with_temp_file() as f:
        yield f


class TestTarUtils:
    def test_list_files_return_list_of_files(self):
        result = sut.list_files(p("example.tar.gz"))
        assert result == ["dir1/", "dir1/file1", "dir1/dir2/", "dir1/dir2/file2"]

    def test_list_files_fails_if_file_not_found(self):
        with pytest.raises(subprocess.CalledProcessError):
            sut.list_files(p("DO_NOT_EXIST"))

    def test_compress_creates_compressed_file(self, destfile):
        files = [p("dir1")]
        sut.compress(files=files, destfile=destfile)
        assert (p_("dir1") + "/") in sut.list_files(destfile)

    def test_compress_fails_if_no_files(self, destfile):
        files = []
        with pytest.raises(subprocess.CalledProcessError):
            sut.compress(files=files, destfile=destfile)

    def test_compress_writes_logs_to_file(self, destfile, logfile):
        files = [p("dir1")]
        sut.compress(files=files, destfile=destfile, logfile=logfile)
        with open(logfile) as f:
            assert len(f.readlines()) == 4
