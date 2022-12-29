from typing import Any
import os


environ = os.environ


def set_environ(x):
    global environ
    environ = x


def reset_environ():
    set_environ(os.environ)


def get(name: str, default: Any = None) -> Any:
    return environ.get(name, default)
