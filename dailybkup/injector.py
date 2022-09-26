import dailybkup.config as configmod
import dailybkup.runner as runnermod
import dailybkup.state as statemod
import dailybkup.compression as compression
import dailybkup.storer as storermod
import dailybkup.fileutils as fileutils
import dailybkup.b2utils as b2utils
from dailybkup import cleaner as cleanermod
from dailybkup import encryption as encryptionmod
import yaml
import datetime
from typing import Optional, Sequence
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
                self._config = configmod.config_builder.build({})
            else:
                with open(self._config_file) as f:
                    d = yaml.load(f, Loader=yaml.Loader)
                    self._config = configmod.config_builder.build(d)
        return self._config


class _Injector():
    """
    Class responsible to inject dependencies to commands.
    """

    _config_loader: _ConfigLoader
    _temp_file_generator_instance: Optional[fileutils.ITempFileGenerator]

    def __init__(self, config_loader: _ConfigLoader):
        self._config_loader = config_loader
        self._temp_file_generator_instance = None

    def temp_file_generator(self) -> fileutils.ITempFileGenerator:
        if self._temp_file_generator_instance is None:
            config = self._config_loader.load()
            self._temp_file_generator_instance = fileutils.TempFileGenerator(
                directory=config.tempdir,
            )
        return self._temp_file_generator_instance

    def compressor(self) -> compression.ICompressor:
        config = self._config_loader.load()
        return compression.TarCompressor(
            config.compression,
            self.temp_file_generator(),
        )

    def b2context(self, bucket_name: str) -> b2utils.B2Context:
        application_key_id = os.environ['DAILYBKUP_B2_APPLICATION_KEY_ID']
        application_key = os.environ['DAILYBKUP_B2_APPLICATION_KEY']
        return b2utils.B2Context(application_key_id, application_key, bucket_name)

    def backup_file_name_generator(self, suffix: str) -> storermod.IBackupFileNameGenerator:
        return storermod.BackupFileNameGenerator(
            suffix=suffix,
            now_fn=datetime.datetime.now,
        )

    def storer(self) -> storermod.IStorer:
        configs = self._config_loader.load().storage
        storers = [
            storermod.build_from_config(
                config,
                l_b2context=self.b2context,
                l_backup_file_name_generator=self.backup_file_name_generator,
            ) for config in configs
        ]
        return storermod.CompositeStorer(storers)

    def cleaner(self) -> cleanermod.ICleaner:
        configs = self._config_loader.load().cleaner
        cleaners = [
            cleanermod.build_from_config(config, l_b2context=self.b2context)
            for config in configs
        ]
        return cleanermod.CompositeCleaner(cleaners)

    def encryptor(self) -> encryptionmod.IEncryptor:
        config = self._config_loader.load().encryption
        return encryptionmod.build_from_config(config, self.temp_file_generator())

    def phase_transition_hooks(self) -> Sequence[statemod.IPhaseTransitionHook]:
        return [
            statemod.CompressedFileCleanupHook(),
            statemod.EncryptedFileCleanupHook(),
            statemod.FinalFileCleanupHook(),
        ]

    def runner(self) -> runnermod.Runner:
        compressor = self.compressor()
        storer = self.storer()
        cleaner = self.cleaner()
        encryptor = self.encryptor()
        phase_transition_hooks = self.phase_transition_hooks()
        LOGGER.info(
            "Loaded runner with: compressor=%s storers=%s encryptor=%s cleaner=%s phase_transition_hooks=%s",
            compressor,
            storer,
            encryptor,
            cleaner,
            phase_transition_hooks,
        )
        return runnermod.Runner(
            compressor=compressor,
            storer=storer,
            cleaner=cleaner,
            encryptor=encryptor,
            phase_transition_hooks=phase_transition_hooks
        )


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
