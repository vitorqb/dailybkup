import dailybkup.tarutils as sut
import pytest
import subprocess
import dailybkup.fileutils as fileutils
from dailybkup.testutils import p, p_
import dailybkup.testutils as testutils
from unittest import mock


@pytest.fixture
def logfile():
    with testutils.with_temp_file() as f:
        yield f


@pytest.fixture
def destfile():
    with testutils.with_temp_file() as f:
        yield f


class TestTarComrpessor:
    def test_creates_compressed_file(self, destfile):
        compressor = sut.TarCompressorRunner()
        compressor(files=[p("dir1/")], destfile=destfile, excludes=[p("dir1/file1")])
        assert sorted(sut.list_files(destfile)) == sorted(
            [
                p_("dir1") + "/",
                p_("dir1/file3"),
                p_("dir1/dir2") + "/",
                p_("dir1/dir2/file2"),
            ]
        )

    def test_fails_if_no_file(self, destfile):
        compressor = sut.TarCompressorRunner()
        with pytest.raises(subprocess.CalledProcessError):
            compressor(files=[], destfile=destfile)

    def test_fails_if_invalid_executable(self, destfile):
        compressor = sut.TarCompressorRunner(executable="DOES_NOT_EXIST")
        with pytest.raises(FileNotFoundError):
            compressor(files=[p("dir1")], destfile=destfile)

    def test_writes_logs_to_file(self, destfile, logfile):
        files = [p("dir1")]
        compressor = sut.TarCompressorRunner(flags=["-v"])
        compressor(files=files, destfile=destfile, logfile=logfile)
        assert fileutils.count_lines(logfile) == 4

    def test_calls_executable_with_custom_flags(self):
        files = ["dir1", "dir2"]
        exclude = ["file1"]
        executable = "FOO"
        compressor = sut.TarCompressorRunner(executable=executable, flags=["--foo"])
        with mock.patch("dailybkup.tarutils.subprocess") as subprocess_mock:
            compressor(
                files=files, destfile="destfile", excludes=exclude, logfile="logfile"
            )
        subprocess_mock.check_output.assert_called_once_with(
            [
                "FOO",
                "--foo",
                "-c",
                f"-fdestfile",
                "--index-file=logfile",
                "--exclude=file1",
                "dir1",
                "dir2",
            ]
        )
