#!/usr/bin/env python3

"""
Unit tests for utils.py
This module contains unit tests for the utility functions
defined in utils.py. It uses unittest and parameterized
to test various scenarios for each function.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


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
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path,  expected):
        """Test access_nested_map with valid paths."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map with invalid paths."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):

    """
    Unit test for the get_json.
    This class tests the function with various URLs
    and checks if it correctly retrieves JSON data.
    It uses mocking to simulate HTTP requests and responses.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, payload):
        """Test get_json with mocked requests."""
        with patch("utils.requests.get") as mock_get:
            mock_result = mock_get.return_value
            mock_result.json.return_value = payload

            result = get_json(test_url)
            self.assertEqual(result, payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Unit test for the memoize decorator.
    This class tests the decorator to ensure it caches
    the results of a method call, preventing \
    redundant computations on subsequent calls.
    """

    def test_memoize(self):
        """Test memoization of a method."""
        class TestClass():
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(TestClass, "a_method", return_value=42) as mock_res:
            instance = TestClass()
            result_1 = instance.a_property
            result_2 = instance.a_property

            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)

            mock_res.assert_called_once()
