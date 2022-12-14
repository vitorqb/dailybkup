from dailybkup.config.common import ConfigBuildState
import dailybkup.config.build_steps as sut
from dailybkup.config.exceptions import MissingConfigKey
import pytest
from typing import Dict, Any


class FakeSettings():
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class FakeBuilder():
    def build(self, d: Dict[str, Any]) -> FakeSettings:
        return FakeSettings(**d)


class TestRequired():
    def test_fails_if_attribute_already_parsed(self):
        state = ConfigBuildState({}, {"foo": "bar"})
        step = sut.Required("foo")
        with pytest.raises(ValueError) as e:
            step(state)
        assert "Duplicated value for foo" in str(e)

    def test_fails_if_attribute_missing(self):
        state = ConfigBuildState({}, {})
        step = sut.Required("foo")
        with pytest.raises(MissingConfigKey) as e:
            step(state)
        assert "foo" in str(e)

    def test_success(self):
        state = ConfigBuildState({"foo": "bar"}, {"bar": "boz"})
        step = sut.Required("foo")
        step(state)
        assert state.unparsed.get("foo") is None
        assert state.parsed.get("bar") == "boz"
        assert state.parsed.get("foo") == "bar"


class TestSubBuilder():
    def test_fails_if_attribute_already_parsed(self):
        state = ConfigBuildState({"foo": {}}, {"foo": "bar"})
        step = sut.SubBuilder("foo", FakeBuilder())
        with pytest.raises(ValueError) as e:
            step(state)
        assert "Duplicated value for foo" in str(e)

    def test_fails_if_missing_attribute(self):
        state = ConfigBuildState({}, {})
        step = sut.SubBuilder("foo", FakeBuilder())
        with pytest.raises(MissingConfigKey) as e:
            step(state)
        assert "foo" in str(e)

    def test_fails_if_value_not_dict(self):
        state = ConfigBuildState({"foo": "bar"}, {})
        step = sut.SubBuilder("foo", FakeBuilder())
        with pytest.raises(ValueError) as e:
            step(state)
        assert "is not a dictionary" in str(e)

    def test_works(self):
        state = ConfigBuildState({"foo": {"bar": 1}}, {})
        step = sut.SubBuilder("foo", FakeBuilder())
        step(state)
        assert state.unparsed.get("foo") is None
        assert isinstance(state.parsed.get("foo"), FakeSettings)
        state.parsed["foo"].kwargs == {"bar": 1}
