import operator
from functools import reduce
from typing import Union


class RecordError(ValueError):
    ...


class RecordFieldError(ValueError):
    ...


def record2field(record: str, obj, *idx: Union[int, slice], **kwargs):
    """
    :param record:
    :param obj:
    :return:
    """
    field_value = operator.itemgetter(*idx)(record)

    if isinstance(field_value, tuple):
        field_value = reduce(operator.add, field_value)

    return obj.from_string(field_value, **kwargs)
