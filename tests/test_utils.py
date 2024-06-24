import unittest
from typing import List, Union
from unittest.mock import MagicMock

from parameterized import parameterized

from igcrepair.reader.utils import get_field


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
