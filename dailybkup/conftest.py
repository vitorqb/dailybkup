import pytest
import dailybkup.injector as injector
import dailybkup.config as configmod
import dailybkup.testutils as testutils
from dailybkup.testutils import p


@pytest.fixture(autouse=True)
def injector_cleanup():
    """
    Ensures we clean up the global setup in the `injector` module.
    """
    try:
        yield
    finally:
        injector.end()


@pytest.fixture
def temp_file():
    with testutils.with_temp_file() as f:
        yield f


@pytest.fixture
def config1():
    with testutils.with_temp_file() as dest_file:
        return configmod.config_builder.build({
            "compressor": {
                "files": [p("afile")],
                "exclude": [],
            },
            "destination": [{
                "type_": "file",
                "path": dest_file
            }]
        })
