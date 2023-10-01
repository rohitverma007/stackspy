import unittest
import sys

sys.path.insert(0, '../')
from stackspy.common import c32helpers

class TestC32Helpers(unittest.TestCase):

    def test_c32_checksum(self):
        self.assertEqual(c32helpers.c32_checksum('123456'), '6dcd4ce23d88e2ee95838f7b014b6284')

    def test_c32_encode(self):
        self.assertEqual(c32helpers.c32_encode('123456'), 'C5SXS')

    def test_c32_decode(self):
        self.assertEqual(c32helpers.c32_decode('C5SXS'), '123456')

    def test_c32_address_decode(self):
        with self.assertRaises(ValueError):
            c32helpers.c32_address_decode('S')
        with self.assertRaises(ValueError):
            c32helpers.c32_address_decode('12345')

    def test_c32_check_decode(self):
        with self.assertRaises(ValueError):
            c32helpers.c32_check_decode('123456789')

    def test_c32_normalize(self):
        self.assertEqual(c32helpers.c32_normalize('oLi'), '011')

    def test_c32_check_encode(self):
        with self.assertRaises(ValueError):
            c32helpers.c32_check_encode(32, '123456')
        with self.assertRaises(ValueError):
            c32helpers.c32_check_encode(-1, '123456')
        with self.assertRaises(ValueError):
            c32helpers.c32_check_encode(1, '12345g')

    def test_c32_address(self):
        with self.assertRaises(ValueError):
            c32helpers.c32_address(1, '12345g')

if __name__ == '__main__':
    unittest.main()