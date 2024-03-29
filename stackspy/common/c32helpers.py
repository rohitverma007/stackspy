import hashlib
import binascii
import base32_lib as base32
import re

C32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';

def c32_checksum(data_hex):
    data_bytes = binascii.unhexlify(data_hex)
    data_hash = hashlib.sha256(hashlib.sha256(data_bytes).digest()).digest()
    checksum = binascii.hexlify(data_hash[:4]).decode()
    return checksum

def c32_encode(hex_data_to_encode):
    return base32.encode(int(hex_data_to_encode, 16)).upper()

def c32_decode(c32_data_to_decode):
    return format(base32.decode(c32_data_to_decode), 'x')

def c32_address_decode(c32_address):
    if len(c32_address) <= 5:
        raise ValueError('Invalid c32 address: invalid length')
    if c32_address[0] != 'S':
        raise ValueError('Invalid c32 address: must start with "S"')
    
    return c32_check_decode(c32_address[1:])

def c32_check_decode(c32_data):
    c32_data = c32_normalize(c32_data)
    data_hex = c32_decode(c32_data[1:])
    version_char = c32_data[0]
    version = C32.index(version_char)
    checksum = data_hex[-8:]
    version_hex = hex(version)[2:]
    if len(version_hex) == 1:
        version_hex = f'0{version_hex}'
    
    if (c32_checksum(f"{version_hex}{data_hex[:-8]}") != checksum):
        raise ValueError('Invalid c32check string: checksum mismatch')
    
    return [version, data_hex[:-8]]


def c32_normalize(c32_input):
    return c32_input.upper().replace("O", "0").replace("L", "1").replace("I", "1")



def c32_check_encode(version_enum, data):
    version = version_enum.value
    if version < 0 or version >= 32:
        raise ValueError('Invalid version (must be between 0 and 31)')
    if not re.match(r'^[0-9a-fA-F]*$', data):
        raise ValueError('Invalid data (not a hex string)')

    data = data.lower()
    if len(data) % 2 != 0:
        data = f'0{data}'

    versionHex = hex(version)[2:]
    if len(versionHex) == 1:
        versionHex = f'0{versionHex}'

    checksumHex = c32_checksum(f'{versionHex}{data}')
    c32str = c32_encode(f'{data}{checksumHex}')

    return f'{C32[version]}{c32str}'

def c32_address(version, hash160hex):
    if not re.match(r'^[0-9a-fA-F]{40}$', hash160hex):
        raise ValueError('Invalid argument: not a hash160 hex string')
    
    c32_string = c32_check_encode(version, hash160hex)
    return f'S{c32_string}'