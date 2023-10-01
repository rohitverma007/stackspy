import unittest
import c32helpers

class TestC32Helpers(unittest.TestCase):

    def test_c32_checksum(self):
        self.assertEqual(c32helpers.c32_checksum('123456'), 'a176f6b242f7c2e6a324fca5f9794d3a')

    def test_c32_encode(self):
        self.assertEqual(c32helpers.c32_encode('123456'), 'C32')

    def test_c32_decode(self):
        self.assertEqual(c32helpers.c32_decode('C32'), '123456')

    def test_c32_address_decode(self):
        self.assertEqual(c32helpers.c32_address_decode('S123456'), ['1', '23456'])

    def test_c32_check_decode(self):
        self.assertEqual(c32helpers.c32_check_decode('123456'), ['1', '23456'])

    def test_c32_normalize(self):
        self.assertEqual(c32helpers.c32_normalize('123456'), '123456')

    def test_c32_check_encode(self):
        self.assertEqual(c32helpers.c32_check_encode(1, '23456'), 'S123456')

    def test_c32_address(self):
        self.assertEqual(c32helpers.c32_address(1, '23456'), 'S123456')

if __name__ == '__main__':
    unittest.main()