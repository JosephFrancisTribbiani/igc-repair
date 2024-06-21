import re
from abc import ABCMeta, abstractmethod

from .utils import RecordFieldError


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
        

class StringRecordField(RecordField):
    PATTERN: re.Pattern = NotImplemented

    def __init__(self, value: str) -> None:
        
        self._value: str = NotImplemented
        self.value = value

    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value) -> None:
        if not (
            isinstance(value, str)
            and re.fullmatch(pattern=self.PATTERN, string=value)
        ):
            raise RecordFieldError('Формат поля %s не соответствует формату %s.', self.__class__.__name__, self.PATTERN)
        self._value = value.upper()

    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def from_string(cls, string: str):
        super().from_string(string)
        return cls(value=string)


class RecordLiteral(StringRecordField):
    PATTERN: re.Pattern = re.compile(pattern=r'[AGHIJCBEFKLD]{1}', flags=re.IGNORECASE)
    

class ManufacturerCode(StringRecordField):
    PATTERN: re.Pattern = re.compile(pattern=r'[0-9A-Z]{3}', flags=re.IGNORECASE)


class UniqueID(StringRecordField):
    PATTERN: re.Pattern = re.compile(pattern=r'[0-9A-Z]{3}', flags=re.IGNORECASE)

    
class IDExtension(StringRecordField):
    PATTERN: re.Pattern = re.compile(pattern=r'[0-9A-Z]*', flags=re.IGNORECASE)

    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value) -> None:
        if not (
            isinstance(value, str)
            and re.fullmatch(pattern=self.PATTERN, string=value)
        ):
            raise RecordFieldError('Формат поля %s не соответствует формату %s.', self.__class__.__name__, self.PATTERN)
        self._value = value


class Validity(StringRecordField):
    """
    Use A for a 3D fix and V for a 2D fix (no GPS altitude) or for no GPS data (pressure altitude data must continue
    to be recorded using times from the RTC).
    """
    PATTERN: re.Pattern = re.compile(pattern=r'[AV]{1}', flags=re.IGNORECASE)
