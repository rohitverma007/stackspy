from secp256k1 import PrivateKey, PublicKey
import struct
from common.helpers import StacksMessageType
def ensure_uint53(n):
    MAX_SAFE_INTEGER = 9007199254740991
    if n < 0 or n > MAX_SAFE_INTEGER or n != int(n):
        raise ValueError('value out of range')

def encode(number, bytes=None, offset=0):
    """Encode an integer using a format similar to Bitcoin's variable-length integers"""

    if bytes is None:
        # Calculate the encoding length based on the number and allocate bytes
        length = 1 if number < 0xfd else 3 if number <= 0xffff else 5 if number <= 0xffffffff else 9
        bytes = bytearray(length)

    # 8 bit
    if number < 0xfd:
        struct.pack_into('<B', bytes, offset, number)

    # 16 bit
    elif number <= 0xffff:
        struct.pack_into('<B', bytes, offset, 0xfd)
        struct.pack_into('<H', bytes, offset + 1, number)

    # 32 bit
    elif number <= 0xffffffff:
        struct.pack_into('<B', bytes, offset, 0xfe)
        struct.pack_into('<I', bytes, offset + 1, number)

    # 64 bit
    else:
        struct.pack_into('<B', bytes, offset, 0xff)
        struct.pack_into('<I', bytes, offset + 1, number & 0xffffffff)
        struct.pack_into('<I', bytes, offset + 5, number >> 32)

    return bytes


def utf8_to_bytes(s):
    """Convert string to utf-8 bytes"""
    return s.encode('utf-8')


def concat_bytes(*args):
    """Concatenate bytes"""
    return b''.join(args)


def encode_message(message, prefix='\x17Stacks Signed Message:\n'):
    """Encode message for sha256 hashing"""

    # Convert message to bytes if it is a string
    if isinstance(message, str):
        message_bytes = utf8_to_bytes(message)
    elif isinstance(message, bytes):
        message_bytes = message
    else:
        raise TypeError("message must be string or bytes")

    # Encode the length of the message bytes
    encoded_length = encode(len(message_bytes))

    # Concatenate prefix bytes, encoded length, and message bytes
    return concat_bytes(utf8_to_bytes(prefix), encoded_length, message_bytes)


def read_uint8(bytes_, offset=0):
    return bytes_[offset]

def read_uint16le(bytes_, offset=0):
    return struct.unpack_from('<H', bytes_, offset)[0]

def read_uint32le(bytes_, offset=0):
    return struct.unpack_from('<I', bytes_, offset)[0]

def decode(bytes_, offset=0):
    first = read_uint8(bytes_, offset)
    if first < 0xfd:
        return first
    elif first == 0xfd:
        return read_uint16le(bytes_, offset + 1)
    elif first == 0xfe:
        return read_uint32le(bytes_, offset + 1)
    else:
        lo = read_uint32le(bytes_, offset + 1)
        hi = read_uint32le(bytes_, offset + 5)
        number = hi * 0x0100000000 + lo
        ensure_uint53(number)
        return number

def decode_message(encoded_message, prefix = '\x17Stacks Signed Message:\n'):
    prefix_byte_length = len(utf8_to_bytes(prefix))
    message_without_chain_prefix = encoded_message[prefix_byte_length:]
    decoded = decode(message_without_chain_prefix)
    var_int_length = len(encode(decoded))
    return message_without_chain_prefix[var_int_length:]  # Remove the varint prefix

def sign_message_hash_rsv(message_hash, private_key):
    private_key = compress_key_if_needed(private_key)
    privkey = PrivateKey(bytes(bytearray.fromhex(private_key)), raw=True)
    unserialized_signature = privkey.ecdsa_sign_recoverable(
        bytes(bytearray.fromhex(message_hash)), raw=True)
    message_signature, recovery_id = privkey.ecdsa_recoverable_serialize(
        unserialized_signature)
    rsv_signature = message_signature+recovery_id.to_bytes(1, 'big')

    return {
        "signature": rsv_signature.hex(),
        "publicKey": privkey.pubkey.serialize().hex()
    }

def compress_key_if_needed(private_key):
    byte_length = len(bytearray.fromhex(private_key))
    if byte_length == 33 and private_key[-2:] == "01":
        return private_key[:-2]
    else:
        return private_key
        

def sign_with_key(message_hash, private_key):
    private_key = compress_key_if_needed(private_key)
    privkey = PrivateKey(bytes(bytearray.fromhex(private_key)), raw=True)
    unserialized_signature = privkey.ecdsa_sign_recoverable(
        bytes(bytearray.fromhex(message_hash)), raw=True)
    message_signature, recovery_id = privkey.ecdsa_recoverable_serialize(
        unserialized_signature)
    return {
        "type": StacksMessageType.MessageSignature,
        "data": recovery_id.to_bytes(1, 'big').hex()+message_signature.hex()
    }