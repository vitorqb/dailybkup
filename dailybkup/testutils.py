import yaml
import dailybkup.config as configmod
import os.path
import contextlib
import dailybkup.fileutils as fileutils


def p(path):
    """
    Shortcut function to get the path to a testdata file.
    """
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(f"{root}/testdata/{path}")


def p_(path):
    """
    Same as p, but without leading slash '/'
    """
    return p(path)[1:]


@contextlib.contextmanager
def with_temp_file():
    tempfile = fileutils.TempFileGenerator().gen_name()
    try:
        yield tempfile
    finally:
        try:
            os.remove(tempfile)
        except FileNotFoundError:
            pass


@contextlib.contextmanager
def config_to_file(config: configmod.Config):
    with with_temp_file() as f:
        with open(f, 'w') as f_:
            yaml.safe_dump(configmod.dumper.dump(config), f_)
        yield f
