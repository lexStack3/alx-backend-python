#!/usr/bin/env python3
"""Tests the utils.access_nested_map function."""
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test class for creating test cases on .access_nested_map.
    """
    @parameterized.expand([
        ({'a': 1}, ('a',), 1),
        ({'a': {'b': 2}}, ('a',), {'b': 2}),
        ({'a': {'b': 2}}, ('a', 'b'), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_value):
        """Asserts test case parameters from the parameterized.expand()
        decorator provided.

        Args:
            nested_map (dict): A key value pair for testing.
            path (Sequence): List of key(s) to traverse <nested_map>.
        """
        self.assertEqual(access_nested_map(nested_map, path=path), expected_value)

        @parameterized.expand([
            ({}, ('a',)),
            ({'a': 1}, ('a', 'b')),
        ])
        def test_access_nested_map_exception(self):
            with self.assertRaises(KeyError):
                access_nested_map(nested_map, path)


if __name__ == "__main__":
    unittest.main()
