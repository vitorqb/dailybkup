import dailybkup.runner as runnermod
from typing import Optional


class _Injector():
    """
    Class responsible to inject dependencies to commands.
    """

    def runner(self) -> runnermod.Runner:
        return runnermod.Runner()


_instance: Optional[_Injector] = None


def get() -> _Injector:
    global _instance
    if _instance is None:
        _instance = _Injector()
    return _instance
