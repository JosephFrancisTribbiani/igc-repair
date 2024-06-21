import unittest
from typing import Type

from parameterized import parameterized

from igcrepair.reader.fields import (
    RecordFieldError,
    StringRecordField,
    RecordLiteral,
    ManufacturerCode,
    UniqueID,
    IDExtension,
    Validity,
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
        with self.assertRaisesRegex(RecordFieldError, 'Формат поля .* не соответствует формату .*.'):
            self.FIELD(value)
    
    def base_test_from_string_exception(self, value: str) -> None:
        with self.assertRaisesRegex(RecordFieldError, 'Передаваемое значение должно быть типа <str>.'):
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
