from abc import ABC, abstractmethod
from typing import Sequence, Dict, TypeVar, Type, Any, Generic
import copy


class MissingKey(Exception):
    pass


class UnkownKey(Exception):
    pass


T = TypeVar('T')


class DictBuilder(Generic[T]):
    """
    Builds a class from a dictionary.
    """

    req_fields: Sequence[str]
    opt_fields: Sequence[str]
    cls_: Type[T]

    def __init__(
            self,
            req_fields: Sequence[str],
            opt_fields: Sequence[str],
            cls_: Type[T]
    ):
        self._req_fields = req_fields
        self._opt_fields = opt_fields
        self._cls_ = cls_

    def build(self, dict_: Dict[str, Any]) -> T:
        fields = [*self._req_fields, *self._opt_fields]
        dict_ = copy.deepcopy(dict_)
        kwargs = {}
        for field in fields:
            if field in dict_:
                kwargs[field] = dict_.pop(field)
        unknown_keys = [x for x in dict_.keys()]
        if unknown_keys:
            raise UnkownKey(f"Keys {unknown_keys} are unknown")
        missing_keys = [x for x in self._req_fields if x not in kwargs]
        if missing_keys:
            raise MissingKey(f"Keys {missing_keys} are missing")
        return self._cls_(**kwargs)
