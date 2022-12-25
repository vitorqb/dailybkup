import pytest
from typing import Any, Dict
import dailybkup.storer.config as sut
import dailybkup.config.exceptions as config_exceptions
from dailybkup.testutils import p


config1 = sut.FileStorageConfig(directory=p("out"))
config_dict1: Dict[str, Any] = {
    "type_": "file",
    "directory": p("out"),
}


class TestFileStorageConfigBuilder:
    def test_from_dict(self):
        result = sut.file_storage_config_builder.build(config_dict1)
        assert result == config1

    def test_missing_key(self):
        with pytest.raises(config_exceptions.MissingConfigKey):
            sut.storage_config_builder.build({})

    def test_extra_key(self):
        dict_ = {**config_dict1, "foo": "bar"}
        with pytest.raises(config_exceptions.UnkownConfigKey):
            sut.storage_config_builder.build(dict_)
