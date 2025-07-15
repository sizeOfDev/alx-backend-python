#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import utils
from parameterized import parameterized
from utils import access_nested_map, get_json


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
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
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
        with patch("utils.requests.get") as mock_get:
            mock_result = mock_get.return_value
            mock_result.json.return_value = payload

            result = get_json(test_url)
            self.assertEqual(result, payload)
            mock_get.assert_called_once_with(test_url)
