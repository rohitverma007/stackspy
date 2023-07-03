import struct
import hashlib


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


# encode message
message = "hello"
encoded_message = encode_message(message)

# now hash it
hash_object = hashlib.sha256(encoded_message)
hex_dig = hash_object.hexdigest()
print(hex_dig)

# now sign the message.
