from os import urandom
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.padding import PKCS7

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from binascii import hexlify, unhexlify
from mnemonic import Mnemonic

def generate_mnemonic(bits=256):
    """Generate a mnemonic phrase following BIP39 standards.
    
    Args:
        bits (int): Strength of the mnemonic phrase. Must be multiple of 32.
                    Default is 128.
        
    Returns:
        str: Generated mnemonic phrase.
    """
    if bits % 32 != 0:
        raise ValueError("Strength must be multiple of 32")

    mnemo = Mnemonic(language='english')
    return mnemo.generate(bits)

# Encrypt a raw mnemonic phrase to be password protected
def encrypt_mnemonic(phrase, password, salt=None, iterations=100000, key_len=48):
    # Convert mnemonic to entropy
    try:
        entropy = Mnemonic("english").to_entropy(phrase)
    except:
        raise ValueError("Not a valid bip39 mnemonic")

    # Convert entropy to hex
    entropy_hex = hexlify(entropy)

    # Use PBKDF2 to derive the encryption key, MAC key and IV
    salt = salt if salt else urandom(16)
    # salt = bytes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    kdf = PBKDF2HMAC(
        algorithm=SHA512(),
        length=key_len,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    keys_and_iv = kdf.derive(password.encode())

    enc_key = keys_and_iv[:16]  # AES-128 requires a 16-byte key
    mac_key = keys_and_iv[16:32]
    iv = keys_and_iv[32:48]

    # Apply PKCS7 padding to plaintext
    padder = PKCS7(128).padder()
    padded_data = padder.update(unhexlify(entropy_hex)) + padder.finalize()

    # Encrypt the entropy using AES-128-CBC
    cipher = Cipher(algorithms.AES(enc_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data)

    # Calculate the HMAC of the salt and ciphertext
    hmac_obj = hmac.HMAC(mac_key, hashes.SHA256(), backend=default_backend())
    hmac_obj.update(salt + cipher_text)
    hmac_digest = hmac_obj.finalize()

    # Concatenate the salt, HMAC digest and ciphertext to form the payload
    payload = salt + hmac_digest + cipher_text

    return payload