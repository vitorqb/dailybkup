import pytest
import dailybkup.cleaner.cleaner as cleanermod
import dailybkup.cleaner.config as configmod
from unittest import mock
import dailybkup.cleaner.builder as sut


class TestCleanerBuilder:
    def test_builds_no_op(self):
        builder = sut.CleanerBuilder(mock.Mock())
        cleaner = builder.build(None)
        assert isinstance(cleaner, cleanermod.NoOpCleaner)

    def test_builds_b2_cleaner(self):
        builder = sut.CleanerBuilder(mock.Mock())
        config = configmod.B2CleanerConfig(retain_last=2, bucket="foo")
        cleaner = builder.build(config)
        assert isinstance(cleaner, cleanermod.B2Cleaner)

    @pytest.mark.gdrive
    def test_builds_gdrive_cleaner(self):
        builder = sut.CleanerBuilder(mock.Mock())
        config = configmod.GDriveCleanerConfig(retain_last=2, folder_id="foo")
        cleaner = builder.build(config)
        assert isinstance(cleaner, cleanermod.GDriveCleaner)

    def test_raises_if_unknown(self):
        builder = sut.CleanerBuilder(mock.Mock())
        with pytest.raises(RuntimeError):
            builder.build(mock.Mock())
