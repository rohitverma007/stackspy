from enum import Enum
from bitcoinlib.keys import HDKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from secp256k1 import PrivateKey
from constants import RECOVERABLE_ECDSA_SIG_LENGTH_BYTES, AuthType

PRIVATE_KEY_COMPRESSED_LENGTH = 33
MEMO_MAX_LENGTH_BYTES = 34 
class PayloadType(Enum):
    TokenTransfer = 0x00
    SmartContract = 0x01
    VersionedSmartContract = 0x06
    ContractCall = 0x02
    PoisonMicroblock = 0x03
    Coinbase = 0x04
    CoinbaseToAltRecipient = 0x05

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

def serialize_memo_string(memo_string: str):
    # convert string to bytes
    content_bytes = memo_string["content"].encode('utf-8')
    # pad the hex string to the right
    padded_content = content_bytes.hex().ljust(MEMO_MAX_LENGTH_BYTES * 2, '0')

    return bytearray.fromhex(padded_content)

def is_single_sig(spending_condition):
    return "signature" in spending_condition

def empty_signature_message():
    return {
        "type": StacksMessageType.MessageSignature,
        "data": bytearray(RECOVERABLE_ECDSA_SIG_LENGTH_BYTES).hex()
    }

def sha512_256(data: bytes) -> bytes:
    digest = hashes.Hash(hashes.SHA512_256(), backend=default_backend())
    digest.update(data)
    return digest.finalize()

def left_pad_hex(hex_string: str) -> str:
    return hex_string if len(hex_string) % 2 == 0 else '0' + hex_string    

def is_hex_addy_compressed(hex_address):
    return not hex_address.startswith('04')

def pub_key_from_priv_key(private_key_32_bytes):
    private_key = PrivateKey(privkey=bytes(bytearray.fromhex(get_32_bytes_key(private_key_32_bytes))), raw=True)
    return private_key.pubkey.serialize().hex()

def create_standard_auth(spending_condition):
    return {
        "authType": AuthType.Standard,
        "spendingCondition": spending_condition
    }
