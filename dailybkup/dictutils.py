from typing import Sequence, Dict, TypeVar, Type, Any, Generic, Protocol
import copy
import dataclasses


class MissingKey(Exception):
    pass


class UnkownKey(Exception):
    pass


#
# Types
#
T = TypeVar('T', covariant=True)
G = TypeVar('G', contravariant=True)
H = TypeVar('H')


#
# Protocols
#
class PDictBuilder(Protocol[T]):
    def build(self, dict_: Dict[str, Any]) -> T:
        ...


class PDictDumper(Protocol[G]):
    def dump(self, x: G) -> Dict[str, Any]:
        ...


#
# Classes
#
class DictBuilder(PDictBuilder[H]):
    """
    Builds a class instance from a dictionary.
    """

    _req_fields: Sequence[str]
    _opt_fields: Sequence[str]
    _cls_: Type[H]
    _missing_key_exception: type
    _unknown_key_exception: type

    def __init__(
            self,
            req_fields: Sequence[str],
            opt_fields: Sequence[str],
            cls_: Type[H],
            missing_key_exception: type = MissingKey,
            unknown_key_exception: type = UnkownKey
    ):
        self._req_fields = req_fields
        self._opt_fields = opt_fields
        self._cls_ = cls_
        self._missing_key_exception = missing_key_exception
        self._unknown_key_exception = unknown_key_exception

    def build(self, dict_: Dict[str, Any]) -> H:
        fields = [*self._req_fields, *self._opt_fields]
        dict_ = copy.deepcopy(dict_)
        kwargs = {}
        for field in fields:
            if field in dict_:
                kwargs[field] = dict_.pop(field)
        unknown_keys = [x for x in dict_.keys()]
        if unknown_keys:
            raise self._unknown_key_exception(f"Keys {unknown_keys} are unknown")
        missing_keys = [x for x in self._req_fields if x not in kwargs]
        if missing_keys:
            raise self._missing_key_exception(f"Keys {missing_keys} are missing")
        return self._cls_(**kwargs)


class DictDumper(PDictDumper[H]):
    """
    Dumps a dataclass to a dictionary.
    """

    def dump(self, x) -> Dict[str, Any]:
        return dataclasses.asdict(x)
