import pytest
from unittest import mock
import dailybkup.config.config as sut
import dailybkup.config as configmod
import dailybkup.config.build_steps as bs


class FakeSetting():
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class FakeBuilder():
    def build(self, d):
        return FakeSetting(**d)


class TestTypeDispatcherConfigBuilder:
    def test_builds(self):
        sub_builder = mock.Mock()
        builders = {"foo": sub_builder}
        builder = sut.TypeDispatcherConfigBuilder(builders)
        config = builder.build({"type_": "foo"})
        assert config == sub_builder.build.return_value
        assert sub_builder.build.called_once_with({})

    def test_unknown_type_raises(self):
        builders = {}
        builder = sut.TypeDispatcherConfigBuilder(builders)
        with pytest.raises(ValueError):
            builder.build({"type_": "foo"})

    def test_missing_type_raises(self):
        builders = {}
        builder = sut.TypeDispatcherConfigBuilder(builders)
        with pytest.raises(configmod.MissingConfigKey):
            builder.build({})


class TestGenericBuilder():
    def test_fails_because_unknown_key(self):
        builder = sut.GenericBuilder(FakeSetting)
        with pytest.raises(sut.UnkownConfigKey) as e:
            builder.build({"foo": "bar"})
        assert "foo" in str(e)

    def test_builds_no_step(self):
        builder = sut.GenericBuilder(FakeSetting)
        setting = builder.build({})
        assert setting.kwargs == {}

    def test_fails_because_missing_required_key(self):
        builder = sut.GenericBuilder(FakeSetting, bs.Required("foo"))
        with pytest.raises(sut.MissingConfigKey) as e:
            builder.build({})
        assert "foo" in str(e)

    def test_builds_with_sub_builder(self):
        builder = sut.GenericBuilder(FakeSetting, bs.SubBuilder("foo", FakeBuilder()))
        setting = builder.build({"foo": {"bar": 1}})
        assert setting.kwargs["foo"].kwargs["bar"] == 1
