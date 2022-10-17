import dailybkup.injector.injector as sut
import dailybkup.config as configmod
import dailybkup.testutils as testutils
import dataclasses
import tempfile


class TestConfigLoader():

    def test_loads_config(self, config1: configmod.Config):
        with testutils.config_to_file(config1) as config_file:
            loader = sut._ConfigLoader(config_file)
            assert loader.load() == config1

    def test_temporary_file_generator_reads_from_config(self, config1: configmod.Config):
        with tempfile.TemporaryDirectory() as tempdir:
            config1 = dataclasses.replace(config1, tempdir=tempdir)
            with testutils.config_to_file(config1) as config1_file:
                sut.init(config_file=config1_file)
                temp_file_generator = sut.get().temp_file_generator()
                generated_file = temp_file_generator.gen_name()
                assert tempdir in generated_file
