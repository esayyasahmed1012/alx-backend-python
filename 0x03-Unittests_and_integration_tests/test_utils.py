import unittest
from unittest import  mock
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, map, path, expected):
       """"this is an exception the importd access_nested_map"""
       real_output=access_nested_map(map, path)
       self.assertEqual(real_output, expected)
    @parameterized.expand([
            ({}, ("a, "), "a"),
            ({"a": 1}, ("a", "b"), 1)
        ])
    def test_access_nested_map_exception(self, map, path, expected):
        """this is a test for exception"""
        with self.assertRaises(KeyError) as e:
            access_nested_map(map, path)
            self.assertEqual(expected, e.exception)

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("https://example.com", {"payload":True}),
        ("https://holberon.io", {"payload":False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_response=Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)

if __name__ == "__main__":
    unittest.main()
