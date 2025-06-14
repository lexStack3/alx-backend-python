#!/usr/bin/env python3
"""Tests the utils.access_nested_map function."""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests the utils.access_nested_map function."""

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
        self.assertEqual(access_nested_map(nested_map,
                                           path=path),
                         expected_value)

    @parameterized.expand([
        ({}, ('a',)),
        ({'a': 1}, ('a', 'b')),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Asserts KeyError is raised and message is correct when key is
        missing.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Unit tests the utils.get_json function."""
    @parameterized.expand([
        ('http://example.com', {'payload': True}),
        ('http://holberton.io', {'payload': False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Mocks requests.get and checks returned JSON."""
        mock_res = Mock()
        mock_res.json.return_value = test_payload
        mock_get.return_value = mock_res

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertDictEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit test the utils.memoize decorator."""
    def test_memoize(self):
        """
        Tests the @memoize decorator to ensure that a method is
        only called once and its result is cached for subsequent accesses.

        The test uses on the original method to verify that:
        - The method is called during the first property access.
        - The method is not called again on subsequent accesses.
        - The memoized value is correctly returned both items.
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        inst = TestClass()
        with patch.object(TestClass, 'a_method', return_value=42) as mock_a_meth:
            self.assertEqual(inst.a_property, 42)
            self.assertEqual(inst.a_property, 42)
            mock_a_meth.assert_called_once()


if __name__ == "__main__":
    unittest.main()
