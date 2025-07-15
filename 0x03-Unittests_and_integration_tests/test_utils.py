#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):

    """
    Unit tests for the access_nested_map function.
    This class tests the function with various \
        nested map structures and key paths.
    It checks if the function correctly \
        retrieves values from nested dictionaries
    based on the provided key paths.
    """

    @parameterized.expand([
        ("case 1", {"a": 1}, ("a",), 1),
        ("case 2", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("case 3", {"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, name, nested_map, path,  expected):
        """Run test case: {name}"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)
