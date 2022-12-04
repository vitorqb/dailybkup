import dailybkup.encryption.config as sut
import pytest
import dailybkup.config.exceptions as config_exceptions


class TestEncryptionConfigBuilder:
    def test_password_config_from_dict(self):
        dict_ = {"type_": "password", "password": "123"}
        config = sut.encryption_config_builder.build(dict_)
        expected = sut.PasswordEncryptionConfig(password="123")
        assert config == expected

    def test_unknown_type(self):
        dict_ = {"type_": "foo"}
        with pytest.raises(ValueError):
            sut.encryption_config_builder.build(dict_)

    def test_missing_key(self):
        dict_ = {"type_": "password"}
        with pytest.raises(config_exceptions.MissingConfigKey):
            sut.encryption_config_builder.build(dict_)
