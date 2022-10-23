import yaml
import dailybkup.config as configmod
import os.path
import contextlib
import dailybkup.fileutils as fileutils
import dailybkup.b2utils as b2utils


B2_TEST_BUCKET = "dailybkup-test"


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
        with open(f, "w") as f_:
            yaml.safe_dump(configmod.dumper.dump(config), f_)
        yield f


@contextlib.contextmanager
def b2_test_setup():
    application_key_id = os.environ["DAILYBKUP_B2_APPLICATION_KEY_ID"]
    application_key = os.environ["DAILYBKUP_B2_APPLICATION_KEY"]
    context = b2utils.B2Context(application_key_id, application_key, B2_TEST_BUCKET)
    try:
        yield context
    finally:
        context.delete_all_files()
