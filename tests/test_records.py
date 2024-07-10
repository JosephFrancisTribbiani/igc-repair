import unittest
from parameterized import parameterized
from igcrepair.reader.records import IRecord
from igcrepair.reader.utils import RecordFieldError


class TestIRecord(unittest.TestCase):

    @parameterized.expand(
        [
            ('I023636LAD3737LOD', 2, 'LAD', 36, 36, 'LOD', 37, 37),
            ('i023636Lad3738loD', 2, 'LAD', 36, 36, 'LOD', 37, 38),
        ]
    )
    def test_from_string(
        self,
        string: str,
        expected_length: int,
        ext_1_expected_subtype: str,
        ext_1_expected_start: str,
        ext_1_expected_finish: str,
        ext_2_expected_subtype: str,
        ext_2_expected_start: str,
        ext_2_expected_finish: str,
    ) -> None:
        record = IRecord.from_string(string)
        self.assertEqual(len(record), expected_length)
        ext_1 = record.extensions[0]
        ext_2 = record.extensions[1]
        self.assertEqual(ext_1.subtype.value, ext_1_expected_subtype)
        self.assertEqual(ext_1.start.value, ext_1_expected_start)
        self.assertEqual(ext_1.finish.value, ext_1_expected_finish)
        self.assertEqual(ext_2.subtype.value, ext_2_expected_subtype)
        self.assertEqual(ext_2.start.value, ext_2_expected_start)
        self.assertEqual(ext_2.finish.value, ext_2_expected_finish)

    @parameterized.expand(
        [
            ('I023636LAD3736LOD', 'Начальная позиция должна быть не больше конечной.'),
            ('I023631LAD3738LOD', 'Начальная позиция должна быть не больше конечной.'),
        ]
    )
    def test_from_string_exception(self, string: str, expected_msg: str) -> None:
        with self.assertRaisesRegex(RecordFieldError, expected_msg):
            IRecord.from_string(string)


if __name__ == '__main__':
    unittest.main()
