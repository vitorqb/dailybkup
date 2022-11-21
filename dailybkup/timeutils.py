import datetime
from typing import Callable


NowFn = Callable[[], datetime.datetime]


_now_fn: NowFn = datetime.datetime.now


def set_now_fn(f: NowFn):
    global _now_fn
    _now_fn = f


def now() -> datetime.datetime:
    return _now_fn()
