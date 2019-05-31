from unittest import TestCase
import unittest
from main import add_coordinates

example=[{"name":"place","postcode":"HP201DH"}]

class TestAdd_coordinates(TestCase):
    def test_add_coordinates(self):
        self.assertEqual(len(example),len(add_coordinates(example)))

    def test_add_coordinates_keys_amount(self):
        self.assertFalse(5==5)



if __name__ == '__main__':
    unittest.main()