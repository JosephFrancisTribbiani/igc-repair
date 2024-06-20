import unittest
from unittest.mock import MagicMock
from typing import Optional, Type, Any, List, Union
from fix_igc.reader.records import (
    RecordError, 
    RecordLiteral,
    Latitude,
    Longitude,
    Validity,
    PressureAltitude,
    Record,
    A,
    B,
)
from fix_igc.reader.utils import get_field
from parameterized import parameterized
import datetime


class TestGetField(unittest.TestCase):

    @parameterized.expand(
        [
            ('abcdefghijklmopqrstuvwxyz', [0, ], 'a'),
            ('abcdefghijklmopqrstuvwxyz', [1, ], 'b'),
            ('abcdefghijklmopqrstuvwxyz', [1, 3, ], 'bd'),
            ('abcdefghijklmopqrstuvwxyz', [slice(1, 4)], 'bcd'),
            ('abcdefghijklmopqrstuvwxyz', [slice(1, 4), 5], 'bcdf'),
            ('abcdefghijklmopqrstuvwxyz', [slice(100, None)], ''),
            ('abcdefghijklmopqrstuvwxyz', [slice(100, None), slice(1000, None), ], ''),
        ]
    )
    def test_get_field(self, s: str, idx: List[Union[int, slice]], expected_value: str) -> None:
        mocked_field = MagicMock()
        get_field(s, mocked_field, *idx)
        _, kwargs = mocked_field.call_args
        self.assertEqual(kwargs['value'], expected_value)


class TestRecordLiteral(unittest.TestCase):

    @parameterized.expand(
        [
            ('A', 'A'),
            ('a', 'A'),
            ('B', 'B'),
            ('b', 'B'),
        ]
    )
    def test_record_literal(self, record_literal: str, expected: Optional[str]) -> None:
        record_field = RecordLiteral(value=record_literal)
        self.assertEqual(record_field.value, expected)
        self.assertEqual(record_field(), expected)
        self.assertEqual(str(record_field), expected)

    @parameterized.expand(
        [
            ('L', RecordError),
            (1, RecordError),
            ('AA', RecordError),
            (None, RecordError),
        ]
    )
    def test_record_literal_exception(self, record_literal: str, expected_exception: Type[RecordError]) -> None:
        with self.assertRaises(expected_exception):
            RecordLiteral(value=record_literal)


class TestLatitude(unittest.TestCase):

    @parameterized.expand(
        [
            ('5439791N', '5439791N', 54, 39.791, 'N'),
            ('0100012s', '0100012S', 1, .012, 'S'),
            ('0000001s', '0000001S', 0, .001, 'S'),
            ('0000000s', '0000000S', 0, .0, 'S'),
        ]
    )
    def test_latitude(
        self, 
        latitude: str,
        expected_latitude: str,
        expected_latitude_degrees: int,
        expected_latitude_decimal_minutes: float,
        expected_latitude_literal: str,
    ) -> None:
        record_field = Latitude(value=latitude)
        self.assertEqual(record_field.value, expected_latitude)
        self.assertEqual(record_field(), expected_latitude)
        self.assertEqual(str(record_field), expected_latitude)
        self.assertEqual(record_field.degrees, expected_latitude_degrees)
        self.assertEqual(record_field.decimal_minutes, expected_latitude_decimal_minutes)
        self.assertEqual(record_field.literal, expected_latitude_literal)

    @parameterized.expand(
        [
            ('1234N', RecordError),
            ('1234567A', RecordError),
            ('123A567N', RecordError),
            ('0070000S', RecordError),
        ]
    )
    def test_latitude(self, latitude: str, expected_exception: Type[RecordError]) -> None:
        with self.assertRaises(expected_exception):
            Latitude(value=latitude)


class TestLongitude(unittest.TestCase):

    @parameterized.expand(
        [
            ('03758038E', '03758038E', 37, 58.038, 'E'),
            ('00100001w', '00100001W', 1, .001, 'W'),
            ('00000000w', '00000000W', 0, .0, 'W'),
        ]
    )
    def test_latitude(
        self, 
        longitude: str,
        expected_longitude: str,
        expected_longitude_degrees: int,
        expected_longitude_decimal_minutes: float,
        expected_longitude_literal: str,
    ) -> None:
        record_field = Longitude(value=longitude)
        self.assertEqual(record_field.value, expected_longitude)
        self.assertEqual(record_field(), expected_longitude)
        self.assertEqual(str(record_field), expected_longitude)
        self.assertEqual(record_field.degrees, expected_longitude_degrees)
        self.assertEqual(record_field.decimal_minutes, expected_longitude_decimal_minutes)
        self.assertEqual(record_field.literal, expected_longitude_literal)

    @parameterized.expand(
        [
            ('1234W', RecordError),
            ('12345678N', RecordError),
            ('12370000W', RecordError),
        ]
    )
    def test_longitude(self, longitude: str, expected_exception: Type[RecordError]) -> None:
        with self.assertRaises(expected_exception):
            Longitude(value=longitude)


class TestValidity(unittest.TestCase):

    @parameterized.expand(
        [
            ('A', 'A'),
            ('a', 'A'),
            ('V', 'V'),
            ('v', 'V'),
        ]
    )
    def test_validity(self, validity: str, expected_validity: str) -> None:
        record_field = Validity(value=validity)
        self.assertEqual(record_field.value, expected_validity)
        self.assertEqual(record_field(), expected_validity)
        self.assertEqual(str(record_field), expected_validity)

    @parameterized.expand(
        [
            ('N', RecordError),
            ('AAA', RecordError),
            (None, RecordError),
        ]
    )
    def test_validity_exception(self, validity: Any, expected_exception: Type[RecordError]) -> None:
        with self.assertRaises(expected_exception):
            Validity(value=validity)


class TestPressureAltitude(unittest.TestCase):

    @parameterized.expand(
        [
            ('01564', 1564),
            ('-0564', -564),
            ('-1564', -1564),
        ]
    )
    def test_pressure_altitude(self, pressure_altitude: str, expected_pressure_altitude: int) -> None:
        record_field = PressureAltitude(value=pressure_altitude)
        self.assertEqual(record_field.value, expected_pressure_altitude)
        self.assertEqual(str(record_field), pressure_altitude)

    @parameterized.expand(
        [
            ('123456', RecordError),
            ('-23456', RecordError),
            ('12-45', RecordError),
            ('1234', RecordError),
            ('123F5', RecordError),
        ]
    )
    def test_pressure_altitude_exception(self, pressure_altitude: str, expected_exception: Type[RecordError]) -> None:
        with self.assertRaises(expected_exception):
            PressureAltitude(value=pressure_altitude)


class TestARecord(unittest.TestCase):

    @parameterized.expand(
        [
            ('AXCT54ff734e8955a067', 'A', 'XCT', '54F', 'f734e8955a067', A),
            ('AXCT54f', 'A', 'XCT', '54F', '', A),
            ('aXct54fextention', 'A', 'XCT', '54F', 'extention', A),
        ]
    )
    def test_a_record(
        self, 
        record: str,
        expected_record_literal: str, 
        expected_manufacturer_code: str, 
        expected_unique_id: str, 
        expected_id_extention: str, 
        expected_class: Type[Record],
    ) -> None:
        record_obj = Record(record)
        self.assertEqual(record_obj.record_literal.value, expected_record_literal)
        self.assertEqual(record_obj.manufacturer_code.value, expected_manufacturer_code)
        self.assertEqual(record_obj.unique_id.value, expected_unique_id)
        self.assertEqual(record_obj.id_extention.value, expected_id_extention)
        self.assertEqual(str(record_obj), expected_record_literal + expected_manufacturer_code + expected_unique_id + expected_id_extention)
        self.assertIsInstance(record_obj, expected_class)


class TestBRecord(unittest.TestCase):

    @parameterized.expand(
        [
            ('B1135265439791N03758059EA0018200202', 'B', datetime.time(11, 35, 26), '5439791N', '03758059E', 'A', 182, 202, 'B1135265439791N03758059EA0018200202', B),
        ]
    )
    def test_b_record(
        self,
        record: str,
        expected_record_literal: str,
        expected_time_utc: Type[datetime.time],
        expected_latitude: str,
        expected_longitude: str,
        expected_validity: str,
        expected_pressure_altitude: int,
        expected_gnss_altitude: int,
        expected_b_record: str,
        expected_class: Type[Record],
    ):
        record_obj = Record(record)
        self.assertEqual(record_obj.record_literal.value, expected_record_literal)
        self.assertEqual(record_obj.time_utc.value, expected_time_utc)
        self.assertEqual(record_obj.latitude.value, expected_latitude)
        self.assertEqual(record_obj.longitude.value, expected_longitude)
        self.assertEqual(record_obj.validity.value, expected_validity)
        self.assertEqual(record_obj.pressure_altitude.value, expected_pressure_altitude)
        self.assertEqual(record_obj.gnss_altitude.value, expected_gnss_altitude)
        self.assertEqual(str(record_obj), expected_b_record)
        self.assertIsInstance(record_obj, expected_class)


if __name__ == '__main__':
    unittest.main()
