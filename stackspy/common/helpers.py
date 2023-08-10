import numpy as np
from binascii import unhexlify
from enum import Enum
from bitcoinlib.keys import HDKey

PRIVATE_KEY_COMPRESSED_LENGTH = 33


class StacksMessageType(Enum):
    Address = 0
    Principal = 1
    LengthPrefixedString = 2
    MemoString = 3
    AssetInfo = 4
    PostCondition = 5
    PublicKey = 6
    LengthPrefixedList = 7
    Payload = 8
    MessageSignature = 9
    StructuredDataSignature = 10
    TransactionAuthField = 11


class DerivationType(Enum):
    Wallet = 1
    Data = 2
    Unknown = 3

def get_root_node(wallet):
    return HDKey.from_wif(wallet.root_key)


def compress_private_key(private_key_in_hex):
    private_key_bytes = bytearray.fromhex(private_key_in_hex)
    if len(private_key_bytes) == PRIVATE_KEY_COMPRESSED_LENGTH:
        if(private_key_in_hex[64]+private_key_in_hex[65] != "01"):
            raise Exception("illegal private key hex, 33 bytes but last 2 are not 01")
        return private_key_in_hex
    else:
        if len(private_key_bytes) != 32:
            raise Exception("illegal private key, must be atleast 32 bytes")
        # pad with 1 byte and return
        return private_key_in_hex + "01"

def get_32_bytes_key(private_key_in_hex):
    private_key_bytes = bytearray.fromhex(private_key_in_hex)
    if len(private_key_bytes) == 33:
        return private_key_in_hex[:64]
    else:
        return private_key_in_hex