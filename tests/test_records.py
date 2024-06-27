import unittest

from parameterized import parameterized

from igcrepair.reader.records import A


class TestARecord(unittest.TestCase):

    @parameterized.expand(
        [
            ('AXCT54ff734e8955a067', 'A', 'XCT', '54F', 'f734e8955a067', 'AXCT54Ff734e8955a067'),
            ('AXCT54f', 'A', 'XCT', '54F', '', 'AXCT54F'),
            ('aXct54fextension', 'A', 'XCT', '54F', 'extension', 'AXCT54Fextension'),
        ]
    )
    def test_a_record(
        self, 
        record: str,
        expected_record_literal: str, 
        expected_manufacturer_code: str, 
        expected_unique_id: str, 
        expected_id_extension: str,
        expected_to_string: str,
    ) -> None:
        a = A.from_string(record)
        self.assertEqual(a.record_literal.value, expected_record_literal)
        self.assertEqual(a.manufacturer_code.value, expected_manufacturer_code)
        self.assertEqual(a.unique_id.value, expected_unique_id)
        self.assertEqual(a.id_extension.value, expected_id_extension)
        self.assertEqual(str(a), expected_to_string)


if __name__ == '__main__':
    unittest.main()
