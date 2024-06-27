from abc import ABCMeta, abstractmethod
from typing import Type, Union, Dict

from typing_extensions import Self

from igcrepair.reader.fields import (
    RecordField,
    RecordLiteral,
    ManufacturerCode,
    UniqueID,
    IDExtension,
)
from igcrepair.reader.utils import RecordError, record2field


class Record(object, metaclass=ABCMeta):

    STRUCTURE: Dict[Type[RecordField], Union[int, slice]] = NotImplemented
    
    @abstractmethod
    def __str__(self) -> str:
        ...

    @classmethod
    @abstractmethod
    def from_string(cls, record: str) -> Self:
        ...
    
    def __repr__(self) -> str:
        return str(self)


class A(Record):

    def __init__(
        self,
        manufacturer_code: ManufacturerCode,
        unique_id: UniqueID,
        id_extension: IDExtension,
    ) -> None:

        self.record_literal: RecordLiteral = RecordLiteral(value='A')
        self.manufacturer_code: ManufacturerCode = manufacturer_code
        self.unique_id: UniqueID = unique_id
        self.id_extension: IDExtension = id_extension

    @classmethod
    def from_string(cls, record: str) -> Self:

        if not (
            isinstance(record, str)
            and len(record) >= 7
        ):
            raise RecordError('Запись должна быть типа <str> длиной не менее 7-ми символов.')

        record_literal = record2field(record, RecordLiteral, 0)
        if record_literal.value != 'A':
            raise RecordError(
                'Неправильный тип записи. Должен быть {0}, передан "A".'.format(record_literal.value)
            )

        return cls(
            manufacturer_code=record2field(record, ManufacturerCode, slice(1, 4)),
            unique_id=record2field(record, UniqueID, slice(4, 7)),
            id_extension=record2field(record, IDExtension, slice(7, None)),
        )

    def __str__(self) -> str:
        return (
            f'{self.record_literal}'
            f'{self.manufacturer_code}'
            f'{self.unique_id}'
            f'{self.id_extension}'
        )
