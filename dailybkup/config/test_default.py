import dailybkup.config.default as sut
import dailybkup.testutils as tu


class TestStaticDefaultValue:
    def test_simple(self):
        assert sut.StaticDefaultValue(1).value == 1


class TestDefaultFromEnv:
    def test_none(self):
        with tu.mock_environ():
            assert sut.DefaultFromEnv("FOO").value is sut.NO_DEFAULT

    def test_not_none(self):
        with tu.mock_environ() as environ:
            environ["FOO"] = 1
            assert sut.DefaultFromEnv("FOO").value == 1
