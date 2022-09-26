from typing import Any, Dict
from dailybkup.testutils import p
import dailybkup.config as sut
import dataclasses
import pytest
import copy


compression_config_dict1 = {
    "files": ["/foo", "/bar"],
    "exclude": ["/baz"],
    "tar_executable": "special_tar",
}

compression_config1 = sut.CompressionConfig(
    files=["/foo", "/bar"],
    exclude=["/baz"],
    tar_executable="special_tar",
)

storage_config_dict1: Dict[str, Any] = {
    "type_": "file",
    "path": p("out")
}

storage_config1 = sut.FileStorageConfig(path=p("out"))

config_dict1: Dict[str, Any] = {
    "compression": compression_config_dict1,
    "storage": [storage_config_dict1]
}

config1 = sut.Config(
    compression=compression_config1,
    storage=[storage_config1]
)

config_dict2 = {
    **copy.deepcopy(config_dict1),
    "encryption": {
        "type_": "password",
        "password": "123456",
    }
}

config2 = dataclasses.replace(
    config1,
    encryption=sut.PasswordEncryptionConfig(password="123456")
)


class TestCompressionConfig():

    def test_from_dict(self):
        result = sut.compression_config_builder.build(compression_config_dict1)
        assert result == compression_config1

    def test_fails_on_unknown_arg(self):
        with pytest.raises(sut.UnkownConfigKey):
            sut.compression_config_builder.build({"a": "b"})

    def test_raises_on_missing_arg(self):
        with pytest.raises(sut.MissingConfigKey):
            sut.compression_config_builder.build({})


class TestConfig():

    def test_from_dict(self):
        result = sut.config_builder.build(config_dict1)
        assert result == config1

    def test_from_dict_complete(self):
        result = sut.config_builder.build(config_dict2)
        assert result == config2

    @pytest.mark.parametrize("missing_keys", [["storage", "compression"],
                                              ["compression"],
                                              ["storage"]])
    def test_from_dict_missing_key(self, missing_keys):
        dict_ = copy.deepcopy(config_dict1)
        for key in missing_keys:
            dict_.pop(key)
        with pytest.raises(sut.MissingConfigKey):
            sut.config_builder.build(dict_)


class TestFileStorageConfigBuilder():

    def test_from_dict(self):
        result = sut.file_storage_config_builder.build(storage_config_dict1)
        assert result == storage_config1

    def test_missing_key(self):
        with pytest.raises(sut.MissingConfigKey):
            sut.storage_config_builder.build({})

    def test_extra_key(self):
        dict_ = {**storage_config_dict1, "foo": "bar"}
        with pytest.raises(sut.UnkownConfigKey):
            sut.storage_config_builder.build(dict_)


class TestEncryptionConfigBuilder():

    def test_password_config_from_dict(self):
        dict_ = {"type_": "password", "password": "123"}
        config = sut.EncryptionConfigBuilder().build(dict_)
        expected = sut.PasswordEncryptionConfig(password="123")
        assert config == expected

    def test_unknown_type(self):
        dict_ = {"type_": "foo"}
        with pytest.raises(ValueError):
            sut.EncryptionConfigBuilder().build(dict_)

    def test_missing_key(self):
        dict_ = {"type_": "password"}
        with pytest.raises(sut.MissingConfigKey):
            sut.EncryptionConfigBuilder().build(dict_)


class TestCleanerConfigBuilder():

    def test_build_b2_config(self):
        dict_ = {"type_": "b2", "bucket": "foo", "retain_last": 2}
        config = sut.CleanerConfigBuilder().build(dict_)
        expected = sut.B2CleanerConfig(retain_last=2, bucket="foo")
        assert config == expected

    def test_unknown_type(self):
        dict_ = {}
        with pytest.raises(sut.MissingConfigKey):
            sut.CleanerConfigBuilder().build(dict_)

    def test_value_error_if_unknown_type(self):
        dict_ = {"type_": "foo"}
        with pytest.raises(ValueError):
            sut.CleanerConfigBuilder().build(dict_)
