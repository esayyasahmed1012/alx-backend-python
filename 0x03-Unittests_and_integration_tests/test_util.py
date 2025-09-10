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
    def test_nested_app(self, map, path, expected):
       real_output=access_nested_map(map, path)
       self.assertEqual(real_output, expected)


if __name__ == "__main__":
    unittest.main()

