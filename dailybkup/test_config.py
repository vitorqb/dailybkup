import dailybkup.config as sut
import pytest


compressor_config_dict1 = {
    "files": ["/foo", "/bar"],
    "exclude": ["/baz"],
    "tar_executable": "special_tar",
}

compressor_config1 = sut.CompressorConfig(
    files=["/foo", "/bar"],
    exclude=["/baz"],
    tar_executable="special_tar",
)


class TestCompressorConfig():

    def test_from_dict(self):
        result = sut.CompressorConfig.from_dict(compressor_config_dict1)
        assert result == compressor_config1

    def test_fails_on_unknown_arg(self):
        with pytest.raises(sut.UnkownConfigKey):
            sut.CompressorConfig.from_dict({"a": "b"})

    def test_raises_on_missing_arg(self):
        with pytest.raises(sut.MissingConfigKey):
            sut.CompressorConfig.from_dict({})
