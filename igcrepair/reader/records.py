from typing import Tuple, List

from igcrepair.reader.extensions_fields import (
    NumberOfExtensions,
    Extension,
)
from igcrepair.reader.fields import RecordLiteral
from igcrepair.reader.utils import RecordError, record2field


class IRecord:

    RECORD_TYPE: RecordLiteral = RecordLiteral(value='I')

    def __init__(self, *extensions: Extension) -> None:
        self.extensions: Tuple[Extension, ...] = extensions

    def __len__(self) -> int:
        return len(self.extensions)

    def __str__(self) -> str:
        string: str = (
            f'{self.RECORD_TYPE}'
            f'{NumberOfExtensions(value=len(self))}'
        )
        for extension in self.extensions:
            string += str(extension)
        return string

    @classmethod
    def from_string(cls, string: str) -> 'IRecord':
        record_literal: RecordLiteral = record2field(string, RecordLiteral, 0)
        if record_literal.value != cls.RECORD_TYPE.value:
            raise RecordError(
                'Неправильный тип записи. Должен быть "{0}", передан "{1}".'.format(
                    cls.RECORD_TYPE.value, record_literal.value
                )
            )
        n_extensions: NumberOfExtensions = record2field(string, NumberOfExtensions, slice(1, 3))
        extensions: List[Extension] = []
        for i in range(n_extensions.value):
            start = 3 + 7 * i
            finish = start + 7
            extensions.append(record2field(string, Extension, slice(start, finish)))

        return cls(*extensions)
