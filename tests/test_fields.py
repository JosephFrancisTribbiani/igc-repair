import datetime
import unittest
from typing import Type, Any, Union

from parameterized import parameterized

from igcrepair.reader.fields import (
    RecordFieldError,
    StringRecordField,
    RecordLiteral,
    ManufacturerCode,
    UniqueID,
    IDExtension,
    Validity,
    TimeUTC,
    Latitude,
    Longitude,
    PressureAltitude,
    GNSSAltitude,
)


class BaseTestString(unittest.TestCase):

    FIELD: Type[StringRecordField] = NotImplemented
    
    def base_test(self, value: str, excepted_value: str) -> None:
        self._base_test(self.FIELD(value), excepted_value)
        self._base_test(self.FIELD.from_string(value), excepted_value)
    
    def _base_test(self, field: StringRecordField, excepted_value: str) -> None:
        self.assertEqual(field.value, excepted_value)
        self.assertEqual(field(), excepted_value)
        self.assertEqual(str(field), excepted_value)

    def base_test_exception(self, value: str) -> None:
        with self.assertRaisesRegex(RecordFieldError, r'Формат поля .* не соответствует формату .*\.'):
            self.FIELD(value)
    
    def base_test_from_string_exception(self, value: str) -> None:
        with self.assertRaisesRegex(RecordFieldError, r'Передаваемое значение должно быть типа \<str\>\.'):
            self.FIELD.from_string(value)


class TestRecordLiteral(BaseTestString):

    FIELD: Type[StringRecordField] = RecordLiteral

    @parameterized.expand(
        [
            ('A', 'A'),
            ('a', 'A'),
            ('B', 'B'),
            ('b', 'B'),
        ]
    )
    def test(self, value: str, excepted_value: str) -> None:
        super().base_test(value, excepted_value)

    @parameterized.expand(
        [
            ('S', ),
            (1, ),
            ('AA', ),
            (None, ),
        ]
    )
    def test_exception(self, value: str) -> None:
        super().base_test_exception(value)

    @parameterized.expand(
        [
            (1, ),
            (None, ),
        ]
    )
    def test_from_string_exception(self, value: str) -> None:
        super().base_test_from_string_exception(value)


class TestManufacturerCode(BaseTestString):

    FIELD: Type[StringRecordField] = ManufacturerCode

    @parameterized.expand(
        [
            ('Abc', 'ABC'),
            ('a1c', 'A1C'),
            ('X12', 'X12'),
        ]
    )
    def test(self, value: str, excepted_value: str) -> None:
        super().base_test(value, excepted_value)

    @parameterized.expand(
        [
            ('AB', ),
            (1, ),
            ('AAAA', ),
            ('AA2A', ),
            (None, ),
        ]
    )
    def test_exception(self, value: str) -> None:
        super().base_test_exception(value)

    @parameterized.expand(
        [
            (1, ),
            (None, ),
        ]
    )
    def test_from_string_exception(self, value: str) -> None:
        super().base_test_from_string_exception(value)


class TestUniqueID(BaseTestString):

    FIELD: Type[StringRecordField] = UniqueID

    @parameterized.expand(
        [
            ('Abc', 'ABC'),
            ('a1c', 'A1C'),
            ('X12', 'X12'),
        ]
    )
    def test(self, value: str, excepted_value: str) -> None:
        super().base_test(value, excepted_value)

    @parameterized.expand(
        [
            ('AB', ),
            (1, ),
            ('AAAA', ),
            ('AA2A', ),
            (None, ),
        ]
    )
    def test_exception(self, value: str) -> None:
        super().base_test_exception(value)

    @parameterized.expand(
        [
            (1, ),
            (None, ),
        ]
    )
    def test_from_string_exception(self, value: str) -> None:
        super().base_test_from_string_exception(value)


class TestIDExtension(BaseTestString):

    FIELD: Type[StringRecordField] = IDExtension

    @parameterized.expand(
        [
            ('Abc1234asf', 'Abc1234asf'),
            ('', ''),
            ('abc', 'abc'),
        ]
    )
    def test(self, value: str, excepted_value: str) -> None:
        super().base_test(value, excepted_value)

    @parameterized.expand(
        [
            (1, ),
            (True, ),
            (False, ),
            (None, ),
        ]
    )
    def test_exception(self, value: str) -> None:
        super().base_test_exception(value)

    @parameterized.expand(
        [
            (1, ),
            (True, ),
            (False, ),
            (None, ),
        ]
    )
    def test_from_string_exception(self, value: str) -> None:
        super().base_test_from_string_exception(value)


class TestValidity(BaseTestString):

    FIELD: Type[StringRecordField] = Validity

    @parameterized.expand(
        [
            ('A', 'A'),
            ('a', 'A'),
            ('V', 'V'),
            ('v', 'V'),
        ]
    )
    def test(self, value: str, excepted_value: str) -> None:
        super().base_test(value, excepted_value)

    @parameterized.expand(
        [
            ('aa', ),
            ('B', ),
            (1, ),
            (None, ),
            (True, ),
        ]
    )
    def test_exception(self, value: str) -> None:
        super().base_test_exception(value)

    @parameterized.expand(
        [
            (1, ),
            (True, ),
            (False, ),
            (None, ),
        ]
    )
    def test_from_string_exception(self, value: str) -> None:
        super().base_test_from_string_exception(value)


class TestTimeUTC(unittest.TestCase):

    @parameterized.expand(
        [
            (datetime.time(1, 5, 10), '010510'),
            (datetime.time(0, 0, 0), '000000'),
            (datetime.time(23, 59, 59), '235959'),
        ]
    )
    def test(self, value: datetime.time, expected_string_value: str) -> None:
        field = TimeUTC(value)
        self.assertEqual(field.value, value)
        self.assertEqual(str(field), expected_string_value)
        self.assertEqual(field(), expected_string_value)

    @parameterized.expand(
        [
            ('010510', datetime.time(1, 5, 10)),
            ('000000', datetime.time(0, 0, 0)),
            ('235959', datetime.time(23, 59, 59)),
        ]
    )
    def test_from_string(self, string_value: str, expected_value) -> None:
        field = TimeUTC.from_string(string_value)
        self.assertEqual(field.value, expected_value)

    @parameterized.expand(
        [
            ('abc', ),
            (True, ),
            (False, ),
            (None, ),
            (10, ),
            (datetime.datetime(2024, 1, 1, 0, 0, 0), ),
        ]
    )
    def test_exception(self, value: Any) -> None:
        with self.assertRaisesRegex(RecordFieldError, r'Аттрибут класса value должен быть типа datetime\.time.*'):
            TimeUTC(value)

    @parameterized.expand(
        [
            ('123', r'Формат даты для поля .* не соответствует формату .*\.'),
            ('abc', r'Формат даты для поля .* не соответствует формату .*\.'),
            ('1234567', r'Формат даты для поля .* не соответствует формату .*\.'),
            ('010560', r'Формат даты для поля .* не соответствует формату .*\.'),
            ('016000', r'Формат даты для поля .* не соответствует формату .*\.'),
            ('250500', r'Формат даты для поля .* не соответствует формату .*\.'),
            (True, r'Передаваемое значение должно быть типа <str>\.'),
            (False, r'Передаваемое значение должно быть типа <str>\.'),
            (None, r'Передаваемое значение должно быть типа <str>\.'),
            (10, r'Передаваемое значение должно быть типа <str>\.'),
        ]
    )
    def test_from_string_exception(self, value: Any, msg: str) -> None:
        with self.assertRaisesRegex(RecordFieldError, msg):
            TimeUTC.from_string(value)


class TestLatitude(unittest.TestCase):

    @parameterized.expand(
        [
            (0, 0, 0., 0, 0., 'N'),
            (5.1, 5, 6., 6, 0., 'N'),
            (-5.1, 5, 6., 6, 0., 'S'),
            (89.1, 89, 6., 6, 0., 'N'),
            (-89.1, 89, 6., 6, 0., 'S'),
            (38.272689, 38, 16.36134, 16, 21.6804, 'N'),
        ]
    )
    def test(
        self,
        dd: Union[int, float],
        expected_degrees: int,
        expected_decimal_minutes: float,
        expected_minutes: int,
        expected_decimal_seconds: float,
        expected_side: str,
    ) -> None:
        latitude = Latitude(dd)
        self.assertEqual(latitude.degrees, expected_degrees)
        self.assertAlmostEqual(latitude.decimal_minutes, expected_decimal_minutes, 6)
        self.assertEqual(latitude.minutes, expected_minutes)
        self.assertAlmostEqual(latitude.decimal_seconds, expected_decimal_seconds, 6)
        self.assertEqual(latitude.side, expected_side)

    @parameterized.expand(
        [
            (0, 0, 0., 'N', 0.),
            (0, 0, 0., 'S', 0.),
            (0, 6, 0., 'S', -0.1),
            (89, 6, 0., 'N', 89.1),
            (89, 6, 0., 'S', -89.1),
        ]
    )
    def test_from_dms(self, degrees: int, minutes: int, decimal_seconds: float, side: str, expected_dd: float) -> None:
        latitude = Latitude.from_dms(degrees, minutes, decimal_seconds, side)
        self.assertEqual(latitude.dd, expected_dd)

    @parameterized.expand(
        [
            (0, 0., 'N', 0.),
            (0, 0., 'S', 0.),
            (89, 6., 'N', 89.1),
            (89, 6., 'S', -89.1),
        ]
    )
    def test_from_dmm(self, degrees: int, decimal_minutes: float, side: str, expected_dd: float) -> None:
        latitude = Latitude.from_dmm(degrees, decimal_minutes, side)
        self.assertEqual(latitude.dd, expected_dd)

    @parameterized.expand(
        [
            ('0000000N', 0.),
            ('9000000N', 90.),
            ('9000000S', -90.),
            ('8906000N', 89.1),
            ('8906000S', -89.1),
            ('0506000N', 5.1),
            ('0506000S', -5.1),
        ]
    )
    def test_from_string(self, string: str, expected_dd: float) -> None:
        latitude = Latitude.from_string(string)
        self.assertEqual(latitude.dd, expected_dd)

    @parameterized.expand(
        [
            (0., 0, 0, 'S', 'degrees должен быть типа <int>.'),
            ('a', 0, 0, 'S', 'degrees должен быть типа <int>.'),
            (True, 0, 0, 'S', 'degrees должен быть типа <int>.'),
            (False, 0, 0, 'S', 'degrees должен быть типа <int>.'),
            (None, 0, 0, 'S', 'degrees должен быть типа <int>.'),
            (91, 0, 0, 'S', 'degrees должен быть в промежутке'),
            (-1, 0, 0, 'S', 'degrees должен быть в промежутке'),
            (90, 0., 0, 'S', 'minutes должен быть типа <int>.'),
            (90, 'a', 0, 'S', 'minutes должен быть типа <int>.'),
            (90, True, 0, 'S', 'minutes должен быть типа <int>.'),
            (90, False, 0, 'S', 'minutes должен быть типа <int>.'),
            (90, None, 0, 'S', 'minutes должен быть типа <int>.'),
            (90, -1, 0, 'S', 'minutes должен быть в промежутке'),
            (90, 61, 0, 'S', 'minutes должен быть в промежутке'),
            (90, 60, 'a', 'S', 'decimal_seconds должен быть типа <int> или <float>.'),
            (90, 60, True, 'S', 'decimal_seconds должен быть типа <int> или <float>.'),
            (90, 60, False, 'S', 'decimal_seconds должен быть типа <int> или <float>.'),
            (90, 60, None, 'S', 'decimal_seconds должен быть типа <int> или <float>.'),
            (90, 60, -0.0001, 's', 'decimal_seconds должен быть в промежутке'),
            (90, 60, 60.0001, 's', 'decimal_seconds должен быть в промежутке'),
            (90, 60, 60, 0, 'side должен быть типа <str>.'),
            (90, 60, 60, 1., 'side должен быть типа <str>.'),
            (90, 60, 60, True, 'side должен быть типа <str>.'),
            (90, 60, 60, False, 'side должен быть типа <str>.'),
            (90, 60, 60, None, 'side должен быть типа <str>.'),
            (90, 60, 60, 'a', r'side должен быть .{1} или .{1}\. Указан .*\.'),
            (90, 60, 60, 'aaaa', r'side должен быть .{1} или .{1}\. Указан .*\.'),
            (90, 60, 60, '', r'side должен быть .{1} или .{1}\. Указан .*\.'),
            (90, 1, 0.0001, 'S', r'Значение decimal_degrees должно быть в промежутке'),
            (90, 1, 0., 'S', r'Значение decimal_degrees должно быть в промежутке'),
            (90, 0, 0.0001, 'S', r'Значение decimal_degrees должно быть в промежутке'),
        ]
    )
    def test_from_dms_exception(
        self,
        degrees: int,
        minutes: int,
        decimal_seconds: Union[int, float],
        side: str,
        msg: str,
    ) -> None:
        with self.assertRaisesRegex(RecordFieldError, msg):
            Latitude.from_dms(degrees, minutes, decimal_seconds, side)

    @parameterized.expand(
        [
            (0., 0., 's', 'degrees должен быть типа <int>.'),
            ('a', 0., 'S', 'degrees должен быть типа <int>.'),
            (True, 0., 'n', 'degrees должен быть типа <int>.'),
            (False, 0., 'N', 'degrees должен быть типа <int>.'),
            (None, 0., 'S', 'degrees должен быть типа <int>.'),
            (-1, 0., 'S', 'degrees должен быть в промежутке'),
            (91, 0., 'S', 'degrees должен быть в промежутке'),
            (90, 'a', 'S', 'decimal_minutes должен быть типа <int> или <float>.'),
            (90, False, 'S', 'decimal_minutes должен быть типа <int> или <float>.'),
            (90, True, 'S', 'decimal_minutes должен быть типа <int> или <float>.'),
            (90, None, 'S', 'decimal_minutes должен быть типа <int> или <float>.'),
            (90, -0.001, 's', 'decimal_minutes должен быть в промежутке'),
            (90, 90.001, 's', 'decimal_minutes должен быть в промежутке'),
            (90, 0.0001, 'S', r'Значение decimal_degrees должно быть в промежутке'),
            (90, 0.0001, 'n', r'Значение decimal_degrees должно быть в промежутке'),
        ]
    )
    def test_from_dmm_exception(
        self,
        degrees: int,
        decimal_minutes: float,
        side: str,
        msg: str,
    ) -> None:
        with self.assertRaisesRegex(RecordFieldError, msg):
            Latitude.from_dmm(degrees, decimal_minutes, side)

    @parameterized.expand(
        [
            ('0000000W', 'Неправильный формат широты.'),
            ('a000000S', 'Неправильный формат широты.'),
            ('00000000S', 'Неправильный формат широты.'),
            ('9100000S', 'degrees должен быть в промежутке'),
        ]
    )
    def test_from_string_exception(
        self,
        string: str,
        msg: str,
    ) -> None:
        with self.assertRaisesRegex(RecordFieldError, msg):
            Latitude.from_string(string)


class TestLongitude(unittest.TestCase):

    @parameterized.expand(
        [
            ('00000000W', 0.),
            ('18000000E', 180.),
            ('18000000W', -180.),
            ('17906000E', 179.1),
            ('17906000W', -179.1),
        ]
    )
    def test_from_string(self, string: str, expected_dd: float) -> None:
        longitude = Longitude.from_string(string)
        self.assertEqual(longitude.dd, expected_dd)

    @parameterized.expand(
        [
            ('18000000S', 'Неправильный формат долготы.'),
            ('18000001W', 'Значение decimal_degrees должно быть в промежутке'),
        ]
    )
    def test_from_string_exception(
        self,
        string: str,
        msg: str,
    ) -> None:
        with self.assertRaisesRegex(RecordFieldError, msg):
            Longitude.from_string(string)


class TestPressureAltitude(unittest.TestCase):

    @parameterized.expand(
        [
            (0, '00000'),
            (9999, '09999'),
            (-9999, '-9999'),
        ]
    )
    def test_pressure_altitude(self, value: int, expected_str: str) -> None:
        alt = PressureAltitude(value)
        self.assertEqual(str(alt), expected_str)

    @parameterized.expand(
        [
            (0., 'Значение поля PressureAltitude должно быть типа <int>.'),
            ('0', 'Значение поля PressureAltitude должно быть типа <int>.'),
            (None, 'Значение поля PressureAltitude должно быть типа <int>.'),
            (False, 'Значение поля PressureAltitude должно быть типа <int>.'),
            (True, 'Значение поля PressureAltitude должно быть типа <int>.'),
            (99999, 'Значение поля PressureAltitude должно быть в промежутке'),
            (-10000, 'Значение поля PressureAltitude должно быть в промежутке'),
        ]
    )
    def test_pressure_altitude_exception(self, value: int, msg: str) -> None:
        with self.assertRaisesRegex(RecordFieldError, msg):
            PressureAltitude(value)


class TestGNSSAltitude(unittest.TestCase):

    @parameterized.expand(
        [
            (0, '00000'),
            (99999, '99999'),
        ]
    )
    def test_gnss_altitude(self, value: int, expected_str: str) -> None:
        alt = GNSSAltitude(value)
        self.assertEqual(str(alt), expected_str)

    @parameterized.expand(
        [
            (0., 'Значение поля GNSSAltitude должно быть типа <int>.'),
            ('0', 'Значение поля GNSSAltitude должно быть типа <int>.'),
            (None, 'Значение поля GNSSAltitude должно быть типа <int>.'),
            (False, 'Значение поля GNSSAltitude должно быть типа <int>.'),
            (True, 'Значение поля GNSSAltitude должно быть типа <int>.'),
            (-1, 'Значение поля GNSSAltitude должно быть в промежутке'),
            (100000, 'Значение поля GNSSAltitude должно быть в промежутке'),
        ]
    )
    def test_gnss_altitude_exception(self, value: int, msg: str) -> None:
        with self.assertRaisesRegex(RecordFieldError, msg):
            GNSSAltitude(value)
