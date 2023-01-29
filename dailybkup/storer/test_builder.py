from unittest import mock
import dailybkup.storer.config as configmod
import dailybkup.storer.builder as sut
import dailybkup.storer as storermod


class TestStorerBuilder:
    def test_creates_gdrive_storer(self):
        config = configmod.storage_config_builder.build(
            {
                "type_": "google-drive",
                "suffix": "FOO",
                "folder_id": "ID",
            }
        )
        builder = sut.StorerBuilder(mock.Mock(), mock.Mock())
        storer = builder.build(config)
        assert isinstance(storer, storermod.GDriveStorer)
