import pytest
import dailybkup.config as configmod
import dailybkup.compression.config as sut

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


class TestCompressionConfig:
    def test_from_dict(self):
        result = sut.compression_config_builder.build(compression_config_dict1)
        assert result == compression_config1

    def test_fails_on_unknown_arg(self):
        with pytest.raises(configmod.exceptions.UnkownConfigKey):
            sut.compression_config_builder.build({"a": "b"})

    def test_raises_on_missing_arg(self):
        with pytest.raises(configmod.exceptions.MissingConfigKey):
            sut.compression_config_builder.build({})
