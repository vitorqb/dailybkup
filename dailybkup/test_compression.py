import dailybkup.compression as sut
from dailybkup.state import State
import os
import pytest
import tempfile as tempfilemod
from dailybkup.phases import Phase


def p(path):
    """
    Shortcut function to get the path to a testdata file.
    """
    root = os.path.dirname(os.path.realpath(__file__))
    return f"{root}/testdata/{path}"

def p_(path):
    """
    Same as p, but remove leading /
    """
    out: str = p(path)
    if out.startswith("/"):
        out = out[1:]
    return out


@pytest.fixture
def tempfile():
    x = tempfilemod.NamedTemporaryFile().name
    yield x
    try:
        os.remove(x)
    except Exception:
        pass


class TestTarCompressor():

    def test_compresses_to_file(self, tempfile):
        config = sut.CompressorConfig(
            files=[p("file1"), p("dir1")],
            exclude=[p("dir1/dir2")]
        )
        state_1 = State()
        compressor = sut.TarCompressor(config)
        state_2 = compressor.run(state_1)
        assert state_2.last_phase == Phase.COMPRESSION
        assert p_("dir1/") in state_2.files
        assert p_("file1") in state_2.files
        assert p_("dir1/file3") in state_2.files
        assert p_("dir1/dir2/") not in state_2.files
        assert p_("dir1/dir2/file2") not in state_2.files
        assert p_("dir1/file3") in state_2.files
        assert isinstance(state_2.compression_logfile, str)
        assert isinstance(state_2.compressed_file, str)
        assert os.path.isfile(state_2.compressed_file)
