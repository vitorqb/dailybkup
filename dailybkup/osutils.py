import subprocess

from typing import List, Callable, TYPE_CHECKING, Any
if TYPE_CHECKING:
    from mypy_extensions import Arg

if TYPE_CHECKING:
    RunFn = Callable[[Arg(List[str], "args")], None]
else:
    RUnFn = Any


def _run(args: List[str]) -> None:
    subprocess.check_output(args)


_run_fn = _run


def set_run_fn(f: RunFn):
    global _run_fn
    _run_fn = f


def reset_run_fn():
    global _run_fn
    _run_fn = _run


def run(args: List[str]) -> None:
    return _run_fn(args)
