import unittest
from typing import Type
from parameterized import parameterized
from igcrepair.reader.fields import RecordLiteral
from igcrepair.reader.fields import ManufacturerCode
from igcrepair.reader.utils import RecordFieldError


class TestRecordLiteral(unittest.TestCase):

    @parameterized.expand(
        [
            ('A', 'A'),
            ('a', 'A'),
            ('B', 'B'),
            ('b', 'B'),
        ]
    )
    def test_record_literal(self, record_literal: str, expected: str) -> None:
       self._test_record_literal(RecordLiteral(record_literal), expected)
       self._test_record_literal(RecordLiteral.from_string(record_literal), expected)

    def _test_record_literal(self, record_field: Type[RecordLiteral], expected: str) -> None:
        self.assertEqual(record_field.record_literal, expected)
        self.assertEqual(record_field(), expected)
        self.assertEqual(str(record_field), expected)
        
    @parameterized.expand(
        [
            ('S', RecordFieldError),
            (1, RecordFieldError),
            ('AA', RecordFieldError),
            (None, RecordFieldError),
        ]
    )
    def test_record_literal_exception(self, record_literal: str, expected_exception: Type[RecordFieldError]) -> None:
        with self.assertRaisesRegex(expected_exception, 'Не является ни одной из букв'):
            RecordLiteral(record_literal)


class TestManufacturerCode(unittest.TestCase):

    @parameterized.expand(
        [
            ('Abc', 'ABC'),
            ('abc', 'ABC'),
            ('XXX', 'XXX'),
        ]
    )
    def test_manufacturer_code(self, manufacturer_code: str, expected: str) -> None:
        self._test_manufacturer_code(ManufacturerCode(manufacturer_code), expected)
        self._test_manufacturer_code(ManufacturerCode.from_string(manufacturer_code), expected)
    
    def _test_manufacturer_code(self, record_field: Type[ManufacturerCode], expected: str) -> None:
        self.assertEqual(record_field.manufacturer_code, expected)
        self.assertEqual(record_field(), expected)
        self.assertEqual(str(record_field), expected)

    @parameterized.expand(
        [
            ('AB', RecordFieldError),
            (1, RecordFieldError),
            ('AAAA', RecordFieldError),
            ('AA2A', RecordFieldError),
            (None, RecordFieldError),
        ]
    )
    def test_manufacturer_code_exception(self, manufacturer_code: str, expected_exception: Type[RecordFieldError]) -> None:
        with self.assertRaisesRegex(expected_exception, 'Код производителя должен состоять из трех символов {0-9, a-z, A-Z}.'):
            ManufacturerCode(manufacturer_code)

    @parameterized.expand(
        [
            (1, RecordFieldError),
        ]
    )
    def test_manufacturer_code_from_string_exception(self, manufacturer_code: str, expected_exception: Type[RecordFieldError]) -> None:
        with self.assertRaisesRegex(expected_exception, 'Передаваемое значение должно быть типа <str>.'):
            ManufacturerCode.from_string(manufacturer_code)
