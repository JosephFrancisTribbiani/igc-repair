import operator
from functools import reduce
from typing import Union


def get_field(s: str, obj, *idx: Union[int, slice], **kwargs):
    """
    :param s:
    :param idx:
    :return:
    """
    field_value = operator.itemgetter(*idx)(s)

    if isinstance(field_value, tuple):
        field_value = reduce(operator.add, field_value)

    return obj(value=field_value, **kwargs)
