from typing import Optional
import dailybkup.app as app
import dailybkup.finisher as finishermod
import dailybkup.state as statemod
import dailybkup.compression as compression
import dailybkup.storer as storermod
import dailybkup.fileutils as fileutils
import dailybkup.b2utils as b2utils
import dailybkup.pipeline as pipeline
import dailybkup.notifier as notifiermod
import dailybkup.services.email_sender as email_sender_mod
import dailybkup.services.desktop_notifier as desktop_notifier_mod
import dailybkup.tarutils as tarutils
from dailybkup import cleaner as cleanermod
from dailybkup import encryption as encryptionmod
import yaml
import datetime
from typing import Optional, Sequence
import logging
import os.path


LOGGER = logging.getLogger(__name__)


class _ConfigLoader:

    _config_file: str
    _config: Optional[app.config.Config]

    def __init__(self, config_file: str):
        self._config_file = config_file
        self._config = None

    def load(self) -> app.config.Config:
        if self._config is None:
            LOGGER.info(f"Loading config from file {self._config_file}")
            if not os.path.exists(self._config_file):
                self._config = app.config.config_builder.build({})
            else:
                with open(self._config_file) as f:
                    d = yaml.load(f, Loader=yaml.Loader)
                    self._config = app.config.config_builder.build(d)
        return self._config


class _Injector:
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

    def tar_compressor_runner(
        self, executable: str = "tar", flags: Optional[Sequence[str]] = None
    ) -> tarutils.TarCompressorRunner:
        return tarutils.TarCompressorRunner(executable=executable, flags=flags)

    def compressor(self) -> compression.Compressor:
        config = self._config_loader.load()
        tar_compressor_runner = self.tar_compressor_runner(
            config.compression.tar_executable, config.compression.tar_flags
        )
        return compression.TarCompressor(
            config.compression,
            tempFileGenerator=self.temp_file_generator(),
            tar_compressor_runner=tar_compressor_runner,
        )

    def b2context(self, bucket_name: str, prefix: str) -> b2utils.B2Context:
        application_key_id = os.environ["DAILYBKUP_B2_APPLICATION_KEY_ID"]
        application_key = os.environ["DAILYBKUP_B2_APPLICATION_KEY"]
        return b2utils.B2Context(
            application_key_id, application_key, bucket_name, prefix
        )

    def backup_file_name_generator(
        self, suffix: str
    ) -> storermod.IBackupFileNameGenerator:
        return storermod.BackupFileNameGenerator(
            suffix=suffix,
            now_fn=datetime.datetime.now,
        )

    def storer(self) -> storermod.Storer:
        configs = self._config_loader.load().storage
        builder = storermod.StorerBuilder(
            l_b2context=self.b2context,
            l_backup_file_name_generator=self.backup_file_name_generator,
        )
        storers = [builder.build(config) for config in configs]
        return storermod.CompositeStorer(storers)

    def cleaner(self) -> cleanermod.Cleaner:
        builder = cleanermod.CleanerBuilder(l_b2context=self.b2context)
        configs = self._config_loader.load().cleaner
        cleaners = [builder.build(config) for config in configs]
        return cleanermod.CompositeCleaner(cleaners)

    def notifier(self) -> notifiermod.Notifier:
        email_sender_builder = email_sender_mod.EmailSenderBuilder()
        desktop_notifier_builder = desktop_notifier_mod.DesktopNotifierBuilder()
        builder = notifiermod.NotifierBuilder(
            email_sender_builder, desktop_notifier_builder
        )
        configs = self._config_loader.load().notification
        notifiers = [builder.build(config) for config in configs]
        return notifiermod.CompositeNotifier(notifiers)

    def encryptor(self) -> encryptionmod.Encryptor:
        builder = encryptionmod.EncryptorBuilder(self.temp_file_generator())
        config = self._config_loader.load().encryption
        return builder.build(config)

    def finisher(self) -> finishermod.Finisher:
        return finishermod.Finisher()

    def phase_transition_hooks(self) -> Sequence[statemod.IPhaseTransitionHook]:
        return [
            statemod.CompressedFileCleanupHook(),
            statemod.EncryptedFileCleanupHook(),
            statemod.FinalFileCleanupHook(),
        ]

    def pipeline_runner(self) -> pipeline.Runner:
        steps: Sequence[pipeline.PRunnable] = [
            self.compressor(),
            self.encryptor(),
            self.storer(),
            self.cleaner(),
            self.notifier(),
            self.finisher(),
        ]
        hooks = [
            statemod.CompressedFileCleanupHook(),
            statemod.EncryptedFileCleanupHook(),
            statemod.FinalFileCleanupHook(),
        ]
        return pipeline.Runner(steps=steps, hooks=hooks)

    def initial_state(self) -> statemod.State:
        return statemod.State.initial_state()


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
