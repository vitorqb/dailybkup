from typing import Optional, Callable
import dailybkup.b2utils as b2utils
import dailybkup.cleaner.config as configmod
import dailybkup.cleaner.cleaner as cleanermod


class CleanerBuilder:
    def __init__(self, l_b2context: Callable[[str, str], b2utils.B2Context]):
        self._l_b2context = l_b2context

    def build(self, config: Optional[configmod.ICleanerConfig]) -> cleanermod.ICleaner:
        if config is None:
            return cleanermod.NoOpCleaner()
        if isinstance(config, configmod.B2CleanerConfig):
            b2context = self._l_b2context(config.bucket, config.prefix)
            return cleanermod.B2Cleaner(config, b2context=b2context)
        raise RuntimeError(f"Invalid config class {config.__class__}")
