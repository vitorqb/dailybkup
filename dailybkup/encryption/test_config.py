import dailybkup.encryption.config as sut
import pytest
import dailybkup.config.exceptions as config_exceptions
import dailybkup.testutils as tu


class TestEncryptionConfigBuilder:
    def test_password_config_from_dict(self):
        dict_ = {"type_": "password", "password": "123"}
        config = sut.encryption_config_builder.build(dict_)
        expected = sut.PasswordEncryptionConfig(password="123")
        assert config == expected

    def test_password_from_env(self):
        with tu.mock_environ() as environ:
            environ["DAILYBKUP_ENCRYPTION_PASSWORD"] = "123"
            dict_ = {"type_": "password"}
            config = sut.encryption_config_builder.build(dict_)
            assert config.password == "123"

    def test_unknown_type(self):
        with tu.mock_environ():
            dict_ = {"type_": "foo"}
            with pytest.raises(ValueError):
                sut.encryption_config_builder.build(dict_)

    def test_missing_key(self):
        with tu.mock_environ():
            dict_ = {"type_": "password"}
            with pytest.raises(config_exceptions.MissingConfigKey):
                sut.encryption_config_builder.build(dict_)
