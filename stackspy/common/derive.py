from enum import Enum
import hashlib
class DerivationType(Enum):
    Wallet = 1
    Data = 2
    Unknown = 3

WALLET_CONFIG_PATH = "m/44/5757'/0'/1";
STX_DERIVATION_PATH = "m/44'/5757'/0'/0";
DATA_DERIVATION_PATH = "m/888'/0'"

def sha256_digest(data):
    """Create a SHA256 hash of the input data."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data)
    return sha256_hash.digest()

def derive_salt(root_node):

    public_key_hex = root_node.subkey_for_path(DATA_DERIVATION_PATH).public_hex
    public_key_bytes = bytes.fromhex(public_key_hex)
    salt = sha256_digest(public_key_bytes)
    return salt

def derive_wallet_keys(root_node):
    salt = derive_salt(root_node)
    root_key = root_node.wif(is_private=True)
    config_private_key = root_node.subkey_for_path(WALLET_CONFIG_PATH).private_hex

    return salt, root_key, config_private_key