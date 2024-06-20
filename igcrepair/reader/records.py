import re
import operator
from typing import Any, Type, List, Union
from abc import ABCMeta, abstractmethod
import datetime
from .utils import get_field


class RecordError(ValueError):
    ...


class RecordField:

    def __init__(self, value: str) -> None:

        if not isinstance(value, str):
            raise RecordError
        
        self._len: int = len(value)

    def __call__(self) -> Any:
        return self.value

    def __repr__(self) -> Any:
        return self.value
    
    def __str__(self) -> str:
        return self.value
    
    def __len__(self) -> int:
        return self._len


class RecordLiteral(RecordField):

    def __init__(self, value: str) -> None:
        super().__init__(value)
        if not (
            value.upper() in {c.__name__ for c in Record.__subclasses__()}
        ):
            raise RecordError
        self.value: str = value.upper()


class ManufacturerCode(RecordField):

    def __init__(self, value: str) -> None:
        super().__init__(value)
        if not (
            re.fullmatch(pattern=r'[0-9a-zA-Z]{3}', string=value)
        ):
            raise RecordError
        self.value: str = value.upper()


class UniqueID(RecordField):

    def __init__(self, value: str) -> None:
        super().__init__(value)
        if not (
            re.fullmatch(pattern=r'[0-9a-zA-Z]{3}', string=value)
        ):
            raise RecordError
        self.value: str = value.upper()


class IDExtention(RecordField):

    def __init__(self, value: str) -> None:
        super().__init__(value)
        if not (
            re.fullmatch(pattern=r'[0-9A-Z]*', string=value, flags=re.IGNORECASE)
        ):
            raise RecordError
        self.value: str = value


class TimeUTC(RecordField):

    TIME_FORMAT = '%H%M%S'

    def __init__(self, value: str) -> None:
        super().__init__(value)
        try:
            self.value: Type[datetime.time] = datetime.datetime.strptime(value, self.TIME_FORMAT).time()
        except ValueError:
            raise RecordError
        
    def __str__(self) -> str:
        return self.value.strftime(self.TIME_FORMAT)
    

class Latitude(RecordField):

    def __init__(self, value: str) -> None:
        """
        :param value: Valid characters N, S, 0-9. Obtained directly from the same GPS data package that was the source of the UTC 
                      time that is recorded in the same B-record line. If no latitude is obtained from satellite data, pressure 
                      altitude fixing must continue, using times from the RTC. In this case, in B record lines must repeat the 
                      last latitude that was obtained from satellite data, until GPS fixing is regained.
        :return:
        """
        
        super().__init__(value)
        if not (
            re.fullmatch(pattern=r'[0-9]{7}[NS]{1}', string=value, flags=re.IGNORECASE)
        ):
            raise RecordError('Wrong latitude format.')
        
        self.degrees = self._get_degrees(value)
        self.decimal_minutes = self._get_decimal_minutes(value)
        self.literal = self._get_literal(value)
        self.value = str(self)

    def __str__(self) -> str:
        return '{0:02d}{1:05d}{2}'.format(self.degrees, int(self.decimal_minutes * 1000), self.literal)
    
    @staticmethod
    def _get_degrees(value: str) -> int:
        return int(operator.getitem(value, slice(0, 2)))
    
    @staticmethod
    def _get_decimal_minutes(value: str) -> float:
        decimal_minutes = float(int(operator.getitem(value, slice(2, 7))) / 1000)
        if decimal_minutes > 60:
            raise RecordError
        return decimal_minutes
    
    @staticmethod
    def _get_literal(value: str) -> str:
        return operator.getitem(value, 7).upper()
    

class Longitude(RecordField):

    def __init__(self, value: str) -> None:
        """
        :param value: Valid characters E,W, 0-9. Obtained directly from the same GPS data package that was the source of UTC time 
                      that is recorded in the same B-record line. If no longitude is obtained from satellite data, pressure altitude 
                      fixing must continue, using times from the RTC. In this case, in B record lines must repeat the last longitude 
                      that was obtained from satellite data, until GPS fixing is regained.
        :return:
        """
        super().__init__(value)
        if not (
            re.fullmatch(pattern=r'[0-9]{8}[EW]{1}', string=value, flags=re.IGNORECASE)
        ):
            raise RecordError('Wrong longitude format.')
        
        self.degrees = self._get_degrees(value)
        self.decimal_minutes = self._get_decimal_minutes(value)
        self.literal = self._get_literal(value)
        self.value = str(self)

    def __str__(self) -> str:
        return '{0:03d}{1:05d}{2}'.format(self.degrees, int(self.decimal_minutes * 1000), self.literal)
    
    @staticmethod
    def _get_degrees(value: str) -> int:
        return int(operator.getitem(value, slice(0, 3)))
    
    @staticmethod
    def _get_decimal_minutes(value: str) -> float:
        decimal_minutes = float(int(operator.getitem(value, slice(3, 8))) / 1000)
        if decimal_minutes > 60:
            raise RecordError
        return decimal_minutes
    
    @staticmethod
    def _get_literal(value: str) -> str:
        return operator.getitem(value, 8).upper()
        

class Validity(RecordField):

    def __init__(self, value: str) -> None:
        """
        :param value: Use A for a 3D fix and V for a 2D fix (no GPS altitude) or for no GPS data (pressure altitude data must 
                      continue to be recorded using times from the RTC).
        :return:
        """
        super().__init__(value)
        if not (
            value.upper() in {'A', 'V'}
        ):
            raise RecordError
        self.value: str = value.upper()


class PressureAltitude(RecordField):

    def __init__(self, value: str) -> None:
        """
        :param value: Altitude to the ICAO ISA above the 1013.25 HPa sea level datum, valid characters 0-9 and negative sign "-". 
                      Negative values to have negative sign instead of leading zero.
        :return:
        """
        super().__init__(value)
        if not (
            re.fullmatch(pattern=r'[0-]{1}[0-9]{4}', string=value)
        ):
            raise RecordError
        self.value: int = int(value)

    def __str__(self) -> str:
        return '{0:05d}'.format(self.value)
    

class GNSSAltitude(RecordField):

    def __init__(self, value: str) -> None:
        """
        :param value: Altitude above the WGS84 ellipsoid, valid characters 0-9.
        :return:
        """
        super().__init__(value)
        if not (
            re.fullmatch(pattern=r'[0-9]{5}', string=value)
        ):
            raise RecordError
        self.value: int = int(value)

    def __str__(self) -> str:
        return '{0:05d}'.format(self.value)


class Record(object, metaclass=ABCMeta):

    def __new__(cls, record: str):
        if get_field(record, RecordLiteral, 0).value == 'A': return super(Record, cls).__new__(A)
        if get_field(record, RecordLiteral, 0).value == 'B': return super(Record, cls).__new__(B)
        raise RecordError
    
    @abstractmethod
    def __str__(self) -> str:...
    
    def __repr__(self) -> str:
        return str(self)


class A(Record):

    def __init__(self, record: str) -> None:

        if not (isinstance(record, str) and len(record) >= 7):
            raise RecordError

        self.record_literal = get_field(record, RecordLiteral, 0)
        self.manufacturer_code = get_field(record, ManufacturerCode, *self._manufacturer_code_idx)
        self.unique_id = get_field(record, UniqueID, *self._unique_id_idx)
        self.id_extention = get_field(record, IDExtention, *self._id_extention_idx)

    def __str__(self) -> str:
        return (
            f'{self.record_literal}'
            f'{self.manufacturer_code}'
            f'{self.unique_id}'
            f'{self.id_extention}'
        )
    
    @property
    def _manufacturer_code_idx(self) -> Union[int, slice]:
        return [slice(1, 4), ]
    
    @property
    def _unique_id_idx(self) -> Union[int, slice]:
        return [slice(4, 7), ]
    
    @property
    def _id_extention_idx(self) -> Union[int, slice]:
        return [slice(7, None), ]
    

class B(Record):

    def __init__(self, record: str) -> None:

        # Определяем размер записи.
        self._len: int = len(record)
        
        if not (
            isinstance(record, str) 
            and len(self) in {35, 37}
        ):
            raise RecordError
        
        self.record_literal: Type[RecordLiteral] = get_field(record, RecordLiteral, 0)
        self.time_utc: Type[TimeUTC] = get_field(record, TimeUTC, *self._time_utc_idx)
        self.latitude: Type[Latitude] = get_field(record, Latitude, *self._latitude_idx)
        self.longitude: Type[Longitude] = get_field(record, Longitude, *self._longitude_idx)
        self.validity: Type[Validity] = get_field(record, Validity, *self._validity_idx)
        self.pressure_altitude: Type[PressureAltitude] = get_field(record, PressureAltitude, *self._pressure_altitude_idx)
        self.gnss_altitude: Type[GNSSAltitude] = get_field(record, GNSSAltitude, *self._gnss_altitude_idx)

    def __len__(self) -> int:
        return self._len

    def __str__(self) -> str:
        return (
            f'{self.record_literal}'
            f'{self.time_utc}'
            f'{self.latitude}'
            f'{self.longitude}'
            f'{self.validity}'
            f'{self.pressure_altitude}'
            f'{self.gnss_altitude}'
        )
    
    @property
    def _time_utc_idx(self) -> List[Union[int, slice]]:
        return [slice(1, 7), ]
    
    @property
    def _time_utc_idx(self) -> List[Union[int, slice]]:
        return [slice(1, 7), ]
    
    @property
    def _latitude_idx(self) -> List[Union[int, slice]]:
        if len(self) == 35: return [slice(7, 15), ]
        if len(self) == 37: return [slice(7, 15), 35]
        else: raise RecordError

    @property
    def _longitude_idx(self) -> List[Union[int, slice]]:
        if len(self) == 35: return [slice(15, 24), ]
        if len(self) == 37: return [slice(15, 24), 36]
        else: raise RecordError
    
    @property
    def _validity_idx(self) -> List[Union[int, slice]]:
        return [24, ]
    
    @property
    def _pressure_altitude_idx(self) -> Union[int, slice]:
        return [slice(25, 30), ]
    
    @property
    def _gnss_altitude_idx(self) -> Union[int, slice]:
        return [slice(30, 35), ]
