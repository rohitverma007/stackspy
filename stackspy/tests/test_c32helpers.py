import unittest
import c32helpers

class TestC32Helpers(unittest.TestCase):

    def test_c32_checksum(self):
        self.assertEqual(c32helpers.c32_checksum('123456'), 'a176f6b242f7c2e6a324fca5f9794d3a')
        self.assertEqual(c32helpers.c32_checksum('abcdef'), '4ee1b2a2f2180c2e6a324fca5f9794d3a')
        self.assertRaises(ValueError, c32helpers.c32_checksum, '123g56')

    def test_c32_encode(self):
        self.assertEqual(c32helpers.c32_encode('123456'), 'C32')
        self.assertEqual(c32helpers.c32_encode('abcdef'), 'C32F')
        self.assertRaises(ValueError, c32helpers.c32_encode, '123g56')

    def test_c32_decode(self):
        self.assertEqual(c32helpers.c32_decode('C32'), '123456')
        self.assertEqual(c32helpers.c32_decode('C32F'), 'abcdef')
        self.assertRaises(ValueError, c32helpers.c32_decode, 'C32G')

    def test_c32_address_decode(self):
        self.assertEqual(c32helpers.c32_address_decode('S123456'), ['1', '23456'])
        self.assertEqual(c32helpers.c32_address_decode('Sabcdef'), ['a', 'bcdef'])
        self.assertRaises(ValueError, c32helpers.c32_address_decode, '123456')
        self.assertRaises(ValueError, c32helpers.c32_address_decode, 'S123g56')

    def test_c32_check_decode(self):
        self.assertEqual(c32helpers.c32_check_decode('123456'), ['1', '23456'])
        self.assertEqual(c32helpers.c32_check_decode('abcdef'), ['a', 'bcdef'])
        self.assertRaises(ValueError, c32helpers.c32_check_decode, '123g56')

    def test_c32_normalize(self):
        self.assertEqual(c32helpers.c32_normalize('123456'), '123456')
        self.assertEqual(c32helpers.c32_normalize('abcdef'), 'ABCDEF')
        self.assertEqual(c32helpers.c32_normalize('123o56'), '123056')
        self.assertEqual(c32helpers.c32_normalize('123l56'), '123156')
        self.assertEqual(c32helpers.c32_normalize('123i56'), '123156')

    def test_c32_check_encode(self):
        self.assertEqual(c32helpers.c32_check_encode(1, '23456'), 'S123456')
        self.assertEqual(c32helpers.c32_check_encode(10, 'abcdef'), 'SABCDEF')
        self.assertRaises(ValueError, c32helpers.c32_check_encode, 33, '23456')
        self.assertRaises(ValueError, c32helpers.c32_check_encode, 1, '234g56')

    def test_c32_address(self):
        self.assertEqual(c32helpers.c32_address(1, '23456'), 'S123456')
        self.assertEqual(c32helpers.c32_address(10, 'abcdef'), 'SABCDEF')
        self.assertRaises(ValueError, c32helpers.c32_address, 33, '23456')
        self.assertRaises(ValueError, c32helpers.c32_address, 1, '234g56')

if __name__ == '__main__':
    unittest.main()