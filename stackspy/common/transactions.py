from secp256k1 import PrivateKey
from enum import Enum
import base32_lib as base32
import hashlib
from c32helpers import c32_address
from helpers import get_32_bytes_key

class TransactionVersion(Enum):
    Mainnet = 0x00
    Testnet = 0x80

class AddressHashMode(Enum):
    # SingleSigHashMode - hash160(public-key), same as bitcoin's p2pkh
    SerializeP2PKH = 0x00
    # MultiSigHashMode - hash160(multisig-redeem-script), same as bitcoin's multisig p2sh */
    SerializeP2SH = 0x01
    # SingleSigHashMode - hash160(segwit-program-00(p2pkh)), same as bitcoin's p2sh-p2wpkh */
    SerializeP2WPKH = 0x02
    # MultiSigHashMode - hash160(segwit-program-00(public-keys)), same as bitcoin's p2sh-p2wsh */
    SerializeP2WSH = 0x03

class AddressVersion(Enum):
    MainnetSingleSig = 22
    MainnetMultiSig = 20
    TestnetSingleSig = 26
    TestnetMultiSig = 21

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

def get_address_from_private_key(private_key, transaction_version):
    pub_key = pub_key_from_priv_key(private_key)
    return get_address_from_public_key(pub_key, transaction_version)


def get_address_from_public_key(pub_key, transaction_version):
    address_version = address_hash_mode_to_version(AddressHashMode.SerializeP2PKH, transaction_version)
    # bytearray.fromhex(private_key_32_bytes)
    address_dict = address_from_version_hash(address_version, hashlib.new('ripemd160', hashlib.sha256(bytearray.fromhex(pub_key)).digest()).hexdigest())
    address_string = address_to_string(address_dict)
    return address_string

def pub_key_from_priv_key(private_key_32_bytes):
    # public_key = PublicKey()
    private_key = PrivateKey(privkey=bytes(bytearray.fromhex(get_32_bytes_key(private_key_32_bytes))), raw=True)
    return private_key.pubkey.serialize().hex()        


def address_hash_mode_to_version(hash_mode: AddressHashMode, tx_version: TransactionVersion) -> AddressVersion:
    if hash_mode == AddressHashMode.SerializeP2PKH:
        if tx_version == TransactionVersion.Mainnet:
            return AddressVersion.MainnetSingleSig
        elif tx_version == TransactionVersion.Testnet:
            return AddressVersion.TestnetSingleSig
        else:
            raise ValueError(f"Unexpected txVersion {tx_version} for hashMode {hash_mode}")
    elif hash_mode in [AddressHashMode.SerializeP2SH, 
                       AddressHashMode.SerializeP2WPKH, 
                       AddressHashMode.SerializeP2WSH]:
        if tx_version == TransactionVersion.Mainnet:
            return AddressVersion.MainnetMultiSig
        elif tx_version == TransactionVersion.Testnet:
            return AddressVersion.TestnetMultiSig
        else:
            raise ValueError(f"Unexpected txVersion {tx_version} for hashMode {hash_mode}")
    else:
        raise ValueError(f"Unexpected hashMode {hash_mode}")

def address_from_version_hash(version, hash):
    return {
        "type": StacksMessageType.Address,
        "version": version,
        "hash160": hash
    }

def address_to_string(address):
    return c32_address(address["version"], address["hash160"]);

def get_stx_address(account, transaction_version = TransactionVersion.Testnet):
    return get_address_from_private_key(account.stx_private_key, transaction_version)