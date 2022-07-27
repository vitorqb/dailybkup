import dailybkup.dictutils as sut
import dataclasses
import pytest


@dataclasses.dataclass
class MockObject():
    attr1: str
    attr2: str = ""


class TestDictUtils():

    def test_builds_from_req_fields(self):
        builder = sut.DictBuilder(['attr1'], ['attr2'], MockObject)
        dict_ = {"attr1": "foo"}
        assert builder.build(dict_) == MockObject(attr1="foo")

    def test_builds_with_optional_fields(self):
        builder = sut.DictBuilder(['attr1'], ['attr2'], MockObject)
        dict_ = {"attr1": "foo", "attr2": "bar"}
        assert builder.build(dict_) == MockObject(attr1="foo", attr2="bar")

    def test_missing_required_field(self):
        builder = sut.DictBuilder(['attr1'], [], MockObject)
        dict_ = {}
        with pytest.raises(sut.MissingKey):
            builder.build(dict_)

    def test_extra_key(self):
        builder = sut.DictBuilder(['attr1'], [], MockObject)
        dict_ = {"attr1": "foo", "unknown_key": "bar"}
        with pytest.raises(sut.UnkownKey):
            builder.build(dict_)
