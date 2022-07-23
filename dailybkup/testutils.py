import yaml
import dailybkup.config as configmod
import os.path
import tempfile as tempfilemod
import contextlib


def p(path):
    """
    Shortcut function to get the path to a testdata file.
    """
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(f"{root}/../testdata/{path}")


@contextlib.contextmanager
def with_temp_file():
    tempfile = tempfilemod.NamedTemporaryFile().name
    try:
        yield tempfile
    finally:
        os.remove(tempfile)


@contextlib.contextmanager
def config_to_file(config: configmod.Config):
    with with_temp_file() as f:
        with open(f, 'w') as f_:
            yaml.safe_dump(config.to_dict(), f_)
        yield f
