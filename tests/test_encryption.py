import unittest
from stackspy import encryption
import hashlib 
from secp256k1 import PublicKey 

class TestEncryption(unittest.TestCase):
    
    def test_encode(self):
        self.assertEqual(encryption.encode(10), b'\x0a')
        self.assertEqual(encryption.encode(0xfd), b'\xfd\xfd\x00')
        self.assertEqual(encryption.encode(0x10000), b'\xfe\x00\x00\x01\x00')

    def test_utf8_to_bytes(self):
        self.assertEqual(encryption.utf8_to_bytes('test'), b'test')
        self.assertEqual(encryption.utf8_to_bytes(''), b'')

    def test_concat_bytes(self):
        self.assertEqual(encryption.concat_bytes(b'test', b'1', b'2', b'3'), b'test123')
        self.assertEqual(encryption.concat_bytes(), b'')
        
    def test_encode_message(self):
        self.assertEqual(encryption.encode_message("hello"), b'\x17Stacks Signed Message:\n\x05hello')

    def test_decode_message(self):
        message_to_encode = "Hello Stacks From Python".encode('utf-8')
        encoded_message = encryption.encode_message(message_to_encode)
        decoded_message = encryption.decode_message(encoded_message)
        self.assertEqual(message_to_encode, decoded_message)

    def test_decode(self):
        self.assertEqual(encryption.decode(b'\xfc\x01\x00', 0), 252)  # Test for 8 bit
        self.assertEqual(encryption.decode(b'\xfd\x01\x00', 0), 1)  # Test for 16 bit
        self.assertEqual(encryption.decode(b'\xfe\x01\x00\x00\x00', 0), 1)  # Test for 32 bit
        self.assertEqual(encryption.decode(b'\xff\x01\x00\x00\x00\x01\x00\x00\x00', 0), 4294967297)  # Test for 64 bit (Exceeds 32bit limit)
        self.assertEqual(encryption.decode(b'\xfd\x03\x04', 0), 1027)  # Test for 16 bit non-zero offset
        self.assertEqual(encryption.decode(b'\xfe\x03\x04\x00\x00', 0), 1027)  # Test for 32 bit non-zero offset

    def test_sign_message_hash_rsv(self):
        # encode message
        message = "I am signing this now."
        encoded_message = encryption.encode_message(message)
        # hash it
        hash_object = hashlib.sha256(encoded_message)
        hex_dig = hash_object.hexdigest() # df0e4af616093dfbe3dcae834b0482c6f59f5845a1085165c7dc069dbf7a8ab6
        key = 'edf9aee84d9b7abc145504dde6726c64f369d37ee34ded868fabd876c26570bc'
        sig_data = encryption.sign_message_hash_rsv(hex_dig, key)

        # Use the signature to retrieve public key, test that it equals the same as one retreived from private key.
        signature_bytes = bytes(bytearray.fromhex(sig_data["signature"][:-2]))
        rec_id = int(sig_data["signature"][-2:], 16)
        public_key = PublicKey()
        public_key.public_key = public_key.ecdsa_recover(bytes(bytearray.fromhex(hex_dig)),
            public_key.ecdsa_recoverable_deserialize(signature_bytes, rec_id), raw=True)

        self.assertEqual(public_key.serialize().hex(), sig_data["publicKey"])

if __name__ == '__main__':
    unittest.main()