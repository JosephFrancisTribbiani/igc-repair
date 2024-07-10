import datetime
import re
from abc import ABCMeta, abstractmethod
from typing import Union, Tuple

from typing_extensions import Self

from .utils import RecordFieldError


class RecordField(metaclass=ABCMeta):

    def __call__(self) -> str:
        return str(self)

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...
    
    def __len__(self) -> int:
        return len(str(self))
    
    @classmethod
    @abstractmethod
    def from_string(cls, string: str) -> None:
        if not type(string) is str:
            raise RecordFieldError('Передаваемое значение должно быть типа <str>.')


class IntRecordField(RecordField):

    BOUNDS: Tuple[int, int]
    STRING_PATTERN: re.Pattern = NotImplemented

    def __init__(self, value: int) -> None:
        self._value: int = NotImplemented
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:

        if not type(value) is int:
            raise RecordFieldError(
                'Значение поля {0} должно быть типа <int>.'.format(self.__class__.__name__)
            )

        if not self.BOUNDS[0] <= value <= self.BOUNDS[1]:
            raise RecordFieldError(
                'Значение поля {0} должно быть в промежутке [{1}, {2}]. Указано {3}.'.format(
                    self.__class__.__name__, *self.BOUNDS, value
                )
            )

        self._value = value

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        :param string:
        :return:
        """
        super().from_string(string)

        if not re.fullmatch(pattern=cls.STRING_PATTERN, string=string):
            raise RecordFieldError(
                'Формат поля {0} не соответствует формату {1}.'.format(cls.__class__.__name__, cls.STRING_PATTERN)
            )

        value = int(string)
        return cls(value)


class StringRecordField(RecordField):

    STRING_PATTERN: re.Pattern = NotImplemented

    def __init__(self, value: str) -> None:
        self._value: str = NotImplemented
        self.value = value

    @abstractmethod
    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        return self.value

    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value: str) -> None:
        if not (
            type(value) is str
            and re.fullmatch(pattern=self.STRING_PATTERN, string=value)
        ):
            raise RecordFieldError(
                'Формат поля {0} не соответствует формату {1}.'.format(self.__class__.__name__, self.STRING_PATTERN)
            )
        self._value = value.upper()

    @classmethod
    def from_string(cls, string: str) -> Self:
        super().from_string(string)
        return cls(value=string)


class RecordLiteral(StringRecordField):

    STRING_PATTERN: re.Pattern = re.compile(pattern=r'[AGHIJCBEFKLD]{1}', flags=re.IGNORECASE)

    def __repr__(self) -> str:
        return self.value
    

class ManufacturerCode(StringRecordField):

    STRING_PATTERN: re.Pattern = re.compile(pattern=r'[0-9A-Z]{3}', flags=re.IGNORECASE)

    def __repr__(self) -> str:
        return 'MMM'


class UniqueID(StringRecordField):

    STRING_PATTERN: re.Pattern = re.compile(pattern=r'[0-9A-Z]{3}', flags=re.IGNORECASE)

    def __repr__(self) -> str:
        return 'NNN'

    
class IDExtension(StringRecordField):

    STRING_PATTERN: re.Pattern = re.compile(pattern=r'[0-9A-Z]*', flags=re.IGNORECASE)

    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value) -> None:
        if not (
            type(value) is str
            and re.fullmatch(pattern=self.STRING_PATTERN, string=value)
        ):
            raise RecordFieldError(
                'Формат поля {0} не соответствует формату {1}.'.format(self.__class__.__name__, self.STRING_PATTERN)
            )
        self._value = value

    def __repr__(self) -> str:
        return 'TEXTSTRING'


class Validity(StringRecordField):
    """
    Use A for a 3D fix and V for a 2D fix (no GPS altitude) or for no GPS data (pressure altitude data must continue
    to be recorded using times from the RTC).
    """

    STRING_PATTERN: re.Pattern = re.compile(pattern=r'[AV]{1}', flags=re.IGNORECASE)

    def __repr__(self) -> str:
        return self.value


class TimeUTC(RecordField):

    TIME_FORMAT = '%H%M%S'

    def __init__(self, value: datetime.time) -> None:
        if not type(value) is datetime.time:
            raise RecordFieldError(
                'Аттрибут класса value должен быть типа datetime.time. Передан {0}'.format(type(value))
            )
        self.value: datetime.time = value

    def __str__(self) -> str:
        return self.value.strftime(self.TIME_FORMAT)

    def __repr__(self) -> str:
        return 'HHMMSS'

    @classmethod
    def from_string(cls, string: str) -> Self:
        super().from_string(string)
        try:
            if len(string) != 6:
                raise ValueError
            return cls(datetime.datetime.strptime(string, cls.TIME_FORMAT).time())
        except ValueError:
            raise RecordFieldError(
                'Формат даты для поля {0} не соответствует формату {1}.'.format(cls.__class__.__name__, cls.TIME_FORMAT)
            )


class Coordinates(RecordField, metaclass=ABCMeta):

    BOUNDS: Tuple[int, int] = NotImplemented
    NEGATIVE_SIDE: str = NotImplemented
    POSITIVE_SIDE: str = NotImplemented

    def __init__(self, dd: Union[int, float], n_digits: int = 10) -> None:
        """
        :param dd:
        :param n_digits:
        :return:
        """
        self.n_digits: int = n_digits
        self._dd: float = NotImplemented
        self.dd = dd

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @property
    def dd(self) -> float:
        return self._dd

    @dd.setter
    def dd(self, value: Union[int, float]) -> None:
        """
        :param value:
        :return:
        """
        if type(value) not in (int, float):
            raise RecordFieldError('decimal_degrees должен быть типа <int> или <float>.')

        if not self.BOUNDS[0] <= value <= self.BOUNDS[1]:
            raise RecordFieldError(
                'Значение decimal_degrees должно быть в промежутке от [{0}; {1}] градусов.'.format(*self.BOUNDS)
            )

        value = float(value)
        value = round(value, ndigits=self.n_digits)
        self._dd = value

    @property
    def dms(self) -> Tuple[int, int, float, str]:
        return (
            self.degrees,
            self.minutes,
            self.decimal_seconds,
            self.side,
        )

    @property
    def dmm(self) -> Tuple[int, float, str]:
        """
        Возвращаем координаты в формате DMM.
        :return: Градусы, минуты, сторона света.
        """
        return (
            self.degrees,
            self.decimal_minutes,
            self.side,
        )

    @property
    def degrees(self) -> int:
        value = abs(self.dd)
        value = round(value)
        return value

    @property
    def decimal_minutes(self) -> float:
        value = float(60 * (abs(self.dd) - self.degrees))
        value = round(value, ndigits=self.n_digits)
        return value

    @property
    def minutes(self) -> int:
        value = round(self.decimal_minutes)
        return value

    @property
    def decimal_seconds(self) -> float:
        value = float(3600 * (abs(self.dd) - self.degrees) - 60 * self.minutes)
        value = round(value, ndigits=self.n_digits)
        return value

    @property
    def side(self) -> str:
        if self.dd < 0:
            return self.NEGATIVE_SIDE
        return self.POSITIVE_SIDE

    @classmethod
    def _check_degrees(cls, value: int) -> None:
        """
        :param value:
        :return:
        """

        if not type(value) is int:
            raise RecordFieldError('degrees должен быть типа <int>.')

        if not 0 <= value <= cls.BOUNDS[1]:
            raise RecordFieldError('degrees должен быть в промежутке [{0}; {1}].'.format(0, cls.BOUNDS[1]))

    @staticmethod
    def _check_minutes(value: int) -> None:
        """
        :param value:
        :return:
        """

        if not type(value) is int:
            raise RecordFieldError('minutes должен быть типа <int>.')

        if not 0 <= value <= 60:
            raise RecordFieldError('minutes должен быть в промежутке [{0}; {1}].'.format(0, 60))

    @staticmethod
    def _check_decimal_minutes(value: Union[int, float]) -> None:
        """
        :param value:
        :return:
        """
        if not type(value) in (int, float):
            raise RecordFieldError('decimal_minutes должен быть типа <int> или <float>.')

        if not 0 <= value <= 60:
            raise RecordFieldError('decimal_minutes должен быть в промежутке [{0}; {1}].'.format(0, 60))

    @staticmethod
    def _check_decimal_seconds(value: Union[int, float]) -> None:
        """
        :param value:
        :return:
        """

        if not type(value) in (int, float):
            raise RecordFieldError('decimal_seconds должен быть типа <int> или <float>.')

        if not 0 <= value <= 60:
            raise RecordFieldError('decimal_seconds должен быть в промежутке [{0}; {1}].'.format(0, 60))

    @classmethod
    def _check_side(cls, value: str) -> None:
        """
        :param value:
        :return:
        """
        if not type(value) is str:
            raise RecordFieldError('side должен быть типа <str>.')

        if value.upper() not in (cls.NEGATIVE_SIDE, cls.POSITIVE_SIDE):
            raise RecordFieldError(
                'side должен быть {0} или {1}. Указан {2}.'.format(cls.NEGATIVE_SIDE, cls.POSITIVE_SIDE, value)
            )

    @classmethod
    def from_dms(cls, degrees: int, minutes: int, decimal_seconds: Union[int, float], side: str) -> Self:
        """
        :param degrees:
        :param minutes:
        :param decimal_seconds:
        :param side:
        :return:
        """
        cls._check_degrees(degrees)
        cls._check_minutes(minutes)
        cls._check_decimal_seconds(decimal_seconds)
        cls._check_side(side)
        side = side.upper()
        dd = degrees + minutes / 60 + decimal_seconds / 3600
        if side == cls.NEGATIVE_SIDE:
            dd *= -1
        return cls(dd)

    @classmethod
    def from_dmm(cls, degrees: int, decimal_minutes: Union[int, float], side: str) -> Self:
        """
        :param degrees:
        :param decimal_minutes:
        :param side:
        :return:
        """
        cls._check_degrees(degrees)
        cls._check_decimal_minutes(decimal_minutes)
        cls._check_side(side)
        side = side.upper()
        dd = degrees + decimal_minutes / 60
        if side == cls.NEGATIVE_SIDE:
            dd *= -1
        return cls(dd)

    @classmethod
    @abstractmethod
    def from_string(cls, string: str) -> None:
        """
        :param string:
        :return:
        """
        super().from_string(string)


class Latitude(Coordinates):

    BOUNDS: Tuple[int, int] = (-90, 90)
    NEGATIVE_SIDE: str = 'S'
    POSITIVE_SIDE: str = 'N'

    def __str__(self) -> str:
        degrees, decimal_minutes, side = self.dmm
        decimal_minutes = int(decimal_minutes * 1000)
        return '{0:02d}{1:05d}{2}'.format(degrees, decimal_minutes, side)

    def __repr__(self) -> str:
        return 'DDMMmmmN/S'

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        :param string: Valid characters N, S, 0-9. Obtained directly from the same GPS data package that was the source
                       of the UTC time that is recorded in the same B-record line. If no latitude is obtained from
                       satellite data, pressure altitude fixing must continue, using times from the RTC. In this case,
                       in B record lines must repeat the last latitude that was obtained from satellite data, until
                       GPS fixing is regained.
        :return:
        """
        super().from_string(string)
        if not (
            re.fullmatch(pattern=r'[0-9]{7}[NS]{1}', string=string, flags=re.IGNORECASE)
        ):
            raise RecordFieldError('Неправильный формат широты.')
        degrees = int(string[slice(0, 2)])
        decimal_minutes = float(int(string[slice(2, 7)]) / 1000)
        side = string[7].upper()
        return cls.from_dmm(degrees, decimal_minutes, side)


class Longitude(Coordinates):

    BOUNDS: Tuple[int, int] = (-180, 180)
    NEGATIVE_SIDE: str = 'W'
    POSITIVE_SIDE: str = 'E'

    def __str__(self) -> str:
        degrees, decimal_minutes, side = self.dmm
        decimal_minutes = int(decimal_minutes * 1000)
        return '{0:03d}{1:05d}{2}'.format(degrees, decimal_minutes, side)

    def __repr__(self) -> str:
        return 'DDDMMmmmE/W'

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        :param string: Valid characters E,W, 0-9. Obtained directly from the same GPS data package that was the source
                       of UTC time that is recorded in the same B-record line. If no longitude is obtained from
                       satellite data, pressure altitude fixing must continue, using times from the RTC. In this case,
                       in B record lines must repeat the last longitude that was obtained from satellite data, until
                       GPS fixing is regained.
        :return:
        """
        super().from_string(string)
        if not (
                re.fullmatch(pattern=r'[0-9]{8}[WE]{1}', string=string, flags=re.IGNORECASE)
        ):
            raise RecordFieldError('Неправильный формат долготы.')
        degrees = int(string[slice(0, 3)])
        decimal_minutes = float(int(string[slice(3, 8)]) / 1000)
        side = string[8].upper()
        return cls.from_dmm(degrees, decimal_minutes, side)


class PressureAltitude(IntRecordField):

    BOUNDS: Tuple[int, int] = (-9999, 9999)
    STRING_PATTERN: re.Pattern = re.compile(pattern=r'[0-]{1}[0-9]{4}')

    def __repr__(self) -> str:
        return 'PPPPP'

    def __str__(self) -> str:
        return '{0:05d}'.format(self.value)


class GNSSAltitude(IntRecordField):

    BOUNDS: Tuple[int, int] = (0, 99999)
    STRING_PATTERN: re.Pattern = re.compile(pattern=r'[0-9]{5}')

    def __repr__(self) -> str:
        return 'GGGGG'

    def __str__(self) -> str:
        return '{0:05d}'.format(self.value)
