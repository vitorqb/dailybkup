import dailybkup.cleaner.config as sut
import pytest
import dailybkup.config as configmod


class TestCleanerConfigBuilder:
    def test_build_b2_config(self):
        dict_ = {"type_": "b2", "bucket": "foo", "retain_last": 2}
        config = sut.cleaner_config_builder.build(dict_)
        expected = sut.B2CleanerConfig(retain_last=2, bucket="foo")
        assert config == expected

    def test_unknown_type(self):
        dict_ = {}
        with pytest.raises(configmod.exceptions.MissingConfigKey):
            sut.cleaner_config_builder.build(dict_)

    def test_value_error_if_unknown_type(self):
        dict_ = {"type_": "foo"}
        with pytest.raises(ValueError):
            sut.cleaner_config_builder.build(dict_)
