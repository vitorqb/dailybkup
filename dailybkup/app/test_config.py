from typing import Any, Dict
from dailybkup.testutils import p
import dailybkup.app.config as sut
from dailybkup import storer
from dailybkup import encryption as encryptionmod
from dailybkup import compression as compressionmod
import dailybkup.config.exceptions as config_exceptions
import dataclasses
import pytest
import copy


compression_config_dict1 = {
    "files": ["/foo", "/bar"],
    "exclude": ["/baz"],
    "tar_executable": "special_tar",
}

compression_config1 = compressionmod.CompressionConfig(
    files=["/foo", "/bar"],
    exclude=["/baz"],
    tar_executable="special_tar",
)

config_dict1: Dict[str, Any] = {
    "compression": compression_config_dict1,
    "storage": [{"type_": "file", "path": p("out")}],
}

storer_config1 = storer.config.FileStorageConfig(path=p("out"))
storer_config_dict1: Dict[str, Any] = {"type_": "file", "path": p("out")}


config1 = sut.Config(compression=compression_config1, storage=[storer_config1])

config_dict2 = {
    **copy.deepcopy(config_dict1),
    "encryption": {
        "type_": "password",
        "password": "123456",
    },
}

config2 = dataclasses.replace(
    config1, encryption=encryptionmod.PasswordEncryptionConfig(password="123456")
)


class TestConfig:
    def test_from_dict(self):
        result = sut.config_builder.build(config_dict1)
        assert result == config1

    def test_from_dict_complete(self):
        result = sut.config_builder.build(config_dict2)
        assert result == config2

    @pytest.mark.parametrize(
        "missing_keys", [["storage", "compression"], ["compression"], ["storage"]]
    )
    def test_from_dict_missing_key(self, missing_keys):
        dict_ = copy.deepcopy(config_dict1)
        for key in missing_keys:
            dict_.pop(key)
        with pytest.raises(config_exceptions.MissingConfigKey):
            sut.config_builder.build(dict_)
