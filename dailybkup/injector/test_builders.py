import pytest
from dailybkup import config as configmod
from dailybkup import cleaner as cleanermod
from unittest import mock
from dailybkup.injector import _builders as sut


class TestBuildFromConfig():

    def test_builds_no_op(self):
        builder = sut.CleanerBuilder(mock.Mock())
        cleaner = builder.build(None)
        assert isinstance(cleaner, cleanermod.NoOpCleaner)

    def test_builds_b2_cleaner(self):
        builder = sut.CleanerBuilder(mock.Mock())
        config = configmod.B2CleanerConfig(retain_last=2, bucket="foo")
        cleaner = builder.build(config)
        assert isinstance(cleaner, cleanermod.B2Cleaner)

    def test_raises_if_unknown(self):
        builder = sut.CleanerBuilder(mock.Mock())
        with pytest.raises(RuntimeError):
            builder.build(mock.Mock())
