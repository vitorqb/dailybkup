import pytest
from unittest import mock
import dailybkup.config.config as sut
import dailybkup.config as configmod


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
