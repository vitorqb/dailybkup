from unittest import mock
import pytest
import dailybkup.injector as injector
import dailybkup.app as app
import dailybkup.testutils as testutils
import os
from dailybkup.testutils import p
import copy


@pytest.fixture(autouse=True)
def injector_cleanup():
    """
    Ensures we clean up the global setup in the `injector` module.
    """
    try:
        yield
    finally:
        injector.end()


@pytest.fixture(autouse=True)
def mock_google_auth_default():
    """
    Mocks `google.auth.default` for all tests (autouse=True).
    This ensures we never actually authenticate ourselves w/ google,
    and that tests are not actually sending requests.
    """
    # This try-catch allows us to have tests both w/ and w/out optional
    # gdrive dependencies
    try:
        import google.auth  # type: ignore
    except ModuleNotFoundError:
        yield
    else:
        with mock.patch("google.auth.default") as f:
            f.return_value = mock.Mock(), mock.Mock()  # mock tuple as return value
            yield


@pytest.fixture
def temp_file():
    with testutils.with_temp_file() as f:
        yield f


@pytest.fixture
def config1():
    with (
        testutils.with_temp_file() as dest_file,
        testutils.with_temp_dir() as dest_directory,
    ):
        return app.config.config_builder.build(
            {
                "compression": {
                    "files": [p("afile")],
                    "exclude": [],
                },
                "storage": [
                    {
                        "type_": "file",
                        "directory": dest_directory,
                    }
                ],
            }
        )


@pytest.fixture
def wiremock():
    wiremock_port = os.getenv("DAILYBKUP_TEST_WIREMOCK_PORT", 9000)
    wiremock_host = os.getenv("DAILYBKUP_TEST_WIREMOCK_HOST", "http://127.0.0.1")
    wiremock_url = f"{wiremock_host}:{wiremock_port}"
    wiremock = testutils.Wiremock(url=wiremock_url)
    wiremock.clean()
    yield wiremock
    wiremock.clean()
