import datetime
import unittest
from typing import Type, Any

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
