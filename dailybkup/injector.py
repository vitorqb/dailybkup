import dailybkup.runner as runnermod
import dailybkup.compression as compression
from typing import Optional, List


class _Injector():
    """
    Class responsible to inject dependencies to commands.
    """

    def compressor(self) -> compression.ICompressor:
        # TODO - LOAD FROM CONFIG
        files: List[str] = []
        exclude: List[str] = []
        config = compression.CompressorConfig(files=files, exclude=exclude)
        return compression.TarCompressor(config)

    def runner(self) -> runnermod.Runner:
        compressor = self.compressor()
        return runnermod.Runner(compressor=compressor)


_instance: Optional[_Injector] = None


def get() -> _Injector:
    global _instance
    if _instance is None:
        _instance = _Injector()
    return _instance
