import operator
from functools import reduce
from typing import Union


class RecordError(ValueError):
    ...


class RecordFieldError(ValueError):
    ...


def get_field(record: str, obj, *idx: Union[int, slice], **kwargs):
    """
    :param s:
    :param idx:
    :return:
    """
    field_value = operator.itemgetter(*idx)(record)

    if isinstance(field_value, tuple):
        field_value = reduce(operator.add, field_value)

    return obj(value=field_value, **kwargs)


def set_field(record: str, obj, *idx: Union[int, slice], **kwargs) -> str:
    ...
