import dailybkup.config as configmod
import dailybkup.runner as runnermod
import dailybkup.compression as compression
import yaml
from typing import Optional
import logging
import os.path


LOGGER = logging.getLogger(__name__)


class _ConfigLoader():

    _config_file: str
    _config: Optional[configmod.Config]

    def __init__(self, config_file: str):
        self._config_file = config_file
        self._config = None

    def load(self) -> configmod.Config:
        if self._config is None:
            LOGGER.info(f"Loading config from file {self._config_file}")
            if not os.path.exists(self._config_file):
                self._config = configmod.Config.from_dict({})
            else:
                with open(self._config_file) as f:
                    d = yaml.load(f, Loader=yaml.Loader)
                    self._config = configmod.Config.from_dict(d)
        return self._config


class _Injector():
    """
    Class responsible to inject dependencies to commands.
    """

    _config_loader: _ConfigLoader

    def __init__(self, config_loader: _ConfigLoader):
        self._config_loader = config_loader

    def compressor(self) -> compression.ICompressor:
        config = self._config_loader.load()
        return compression.TarCompressor(config.compressor)

    def runner(self) -> runnermod.Runner:
        compressor = self.compressor()
        return runnermod.Runner(compressor=compressor)


_injector: Optional[_Injector] = None


def init(*, config_file) -> None:
    global _injector
    if _injector is not None:
        raise RuntimeError("Injector already initiated")
    _loader = _ConfigLoader(config_file)
    _injector = _Injector(_loader)


def end() -> None:
    global _injector
    _injector = None


def get() -> _Injector:
    global _injector
    if _injector is None:
        raise RuntimeError("Injector has not been initiated.")
    return _injector
