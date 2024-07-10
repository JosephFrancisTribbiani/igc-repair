import re
from abc import ABCMeta, abstractmethod
from typing import Tuple

from igcrepair.reader.constants import EXTENSION_SUBTYPES
from igcrepair.reader.fields import IntRecordField, StringRecordField
from igcrepair.reader.utils import RecordFieldError, record2field


class IntRecordExtensionField(IntRecordField, metaclass=ABCMeta):

    BOUNDS: Tuple[int, int] = (0, 99)
    STRING_PATTERN: re.Pattern = re.compile(pattern=r'[0-9]{2}')

    @abstractmethod
    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        return '{0:02d}'.format(self.value)


class NumberOfExtensions(IntRecordExtensionField):
    def __repr__(self) -> str:
        return 'NN'


class StartByteNumber(IntRecordExtensionField):

    def __repr__(self) -> str:
        return 'SS'


class FinishByteNumber(IntRecordExtensionField):
    def __repr__(self) -> str:
        return 'FF'


class ExtensionSubtype(StringRecordField):

    STRING_PATTERN: re.Pattern = re.compile(r'[a-z0-9*]{3}', flags=re.IGNORECASE)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        if not (
            type(value) is str
            and value.upper() in EXTENSION_SUBTYPES
        ):
            raise RecordFieldError(
                'Не существующий тип дополнения. Указан {0}.'.format(value)
            )
        self._value = value.upper()

    def __repr__(self) -> str:
        return 'CCC'


class Extension:

    def __init__(
        self,
        start: StartByteNumber,
        finish: FinishByteNumber,
        subtype: ExtensionSubtype,
    ) -> None:

        if start.value > finish.value:
            raise RecordFieldError('Начальная позиция должна быть не больше конечной.')

        self.start: StartByteNumber = start
        self.finish: FinishByteNumber = finish
        self.subtype: ExtensionSubtype = subtype

    @classmethod
    def from_string(cls, string: str) -> 'Extension':
        if type(string) is not str:
            raise RecordFieldError('Передаваемое значение должно быть типа <str>. Передан тип {0}'.format(type(string)))
        if len(string) != 7:
            raise RecordFieldError('Длина строки должна быть равна 7.')

        start: StartByteNumber = record2field(string, StartByteNumber, slice(0, 2))
        finish: FinishByteNumber = record2field(string, FinishByteNumber, slice(2, 4))
        subtype: ExtensionSubtype = record2field(string, ExtensionSubtype, slice(4, 7))

        return cls(start, finish, subtype)
