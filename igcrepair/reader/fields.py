import re
from .utils import RecordFieldError
from abc import ABCMeta, abstractmethod


class RecordField(metaclass=ABCMeta):

    def __call__(self) -> str:
        return str(self)

    def __repr__(self) -> str:
        return str(self)
    
    @abstractmethod
    def __str__(self) -> str:...
    
    def __len__(self) -> int:
        return len(str(self))
    
    @classmethod
    def from_string(cls, string: str):
        if not isinstance(string, str):
            raise RecordFieldError('Передаваемое значение должно быть типа <str>.')
        

class RecordLiteral(RecordField):

    LETTERS = {'A', 'G', 'H', 'I', 'J', 'C', 'B', 'E', 'F', 'K', 'L', 'D'}

    def __init__(self, record_literal: str) -> None:
        
        self._record_literal = NotImplemented
        self.record_literal = record_literal
        
    @property
    def record_literal(self) -> str:
        return self._record_literal
    
    @record_literal.setter
    def record_literal(self, value) -> None:
        if not (
            isinstance(value, str)
            and value.upper() in self.LETTERS
        ):
            raise RecordFieldError('Не является ни одной из букв %s' % self.LETTERS)
        self._record_literal = value.upper()

    def __str__(self) -> str:
        return self.record_literal

    @classmethod
    def from_string(cls, string: str):
        super().from_string(string)
        return cls(record_literal=string)
    

class ManufacturerCode(RecordField):

    def __init__(self, manufacturer_code: str) -> None:
        
        self._manufacturer_code = NotImplemented
        self.manufacturer_code = manufacturer_code
        
    @property
    def manufacturer_code(self) -> str:
        return self._manufacturer_code
    
    @manufacturer_code.setter
    def manufacturer_code(self, value) -> None:
        if not (
            isinstance(value, str)
            and re.fullmatch(pattern=r'[0-9A-Z]{3}', string=value, flags=re.IGNORECASE)
        ):
            raise RecordFieldError('Код производителя должен состоять из трех символов {0-9, a-z, A-Z}.')
        self._manufacturer_code = value.upper()

    def __str__(self) -> str:
        return self.manufacturer_code

    @classmethod
    def from_string(cls, string: str):
        super().from_string(string)
        return cls(manufacturer_code=string)
