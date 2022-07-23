import dailybkup.injector as sut
import dailybkup.config as configmod
from dailybkup.testutils import p
import dailybkup.testutils as testutils


class TestConfigLoader():

    def test_loads_config(self, config1: configmod.Config):
        with testutils.config_to_file(config1) as config_file:
            loader = sut._ConfigLoader(config_file)
            assert loader.load() == config1
