import dailybkup.config as configmod
import dailybkup.compression as sut
from dailybkup.state import State
import os
from dailybkup.phases import Phase
from dailybkup.testutils import p, p_


class TestTarCompressor():

    def test_compresses_to_file(self):
        config = configmod.CompressionConfig(
            files=[p("file1"), p("dir1")],
            exclude=[p("dir1/dir2")]
        )
        state_1 = State()
        compressor = sut.TarCompressor(config)
        state_2 = compressor.run(state_1)
        assert state_2.last_phase == Phase.COMPRESSION
        assert p_("dir1") + "/" in state_2.files
        assert p_("file1") in state_2.files
        assert p_("dir1/file3") in state_2.files
        assert p_("dir1/dir2") + "/" not in state_2.files
        assert p_("dir1/dir2/file2") not in state_2.files
        assert p_("dir1/file3") in state_2.files
        assert isinstance(state_2.compression_logfile, str)
        assert isinstance(state_2.compressed_file, str)
        assert state_2.compressed_file == state_2.current_file
        assert os.path.isfile(state_2.compressed_file)
