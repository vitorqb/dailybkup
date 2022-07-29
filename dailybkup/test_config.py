from typing import Any, Dict
from dailybkup.testutils import p
import dailybkup.config as sut
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

destination_config_dict1: Dict[str, Any] = {
    "type_": "file",
    "path": p("out")
}

destination_config1 = sut.FileDestinationConfig(path=p("out"))

config_dict1 = {
    "compression": compression_config_dict1,
    "destination": [destination_config_dict1]
}

config1 = sut.Config(
    compression=compression_config1,
    destination=[destination_config1]
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

    @pytest.mark.parametrize("missing_keys", [["destination", "compression"],
                                              ["compression"],
                                              ["destination"]])
    def test_from_dict_missing_key(self, missing_keys):
        dict_ = copy.deepcopy(config_dict1)
        for key in missing_keys:
            dict_.pop(key)
        with pytest.raises(sut.MissingConfigKey):
            sut.config_builder.build(dict_)


class TestFileDestinationConfigBuilder():

    def test_from_dict(self):
        result = sut.file_destination_config_builder.build(destination_config_dict1)
        assert result == destination_config1

    def test_missing_key(self):
        with pytest.raises(sut.MissingConfigKey):
            sut.destination_config_builder.build({})

    def test_extra_key(self):
        dict_ = {**destination_config_dict1, "foo": "bar"}
        with pytest.raises(sut.UnkownConfigKey):
            sut.destination_config_builder.build(dict_)
