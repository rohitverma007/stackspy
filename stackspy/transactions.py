from secp256k1 import PrivateKey
from enum import Enum
import base32_lib as base32
import hashlib
from common.c32helpers import c32_address
from common.helpers import get_32_bytes_key, StacksMessageType
from common.clarity import prinicpal_cv
from network import StacksMainnet
from common.StacksTransaction import StacksTransaction

MEMO_MAX_LENGTH_BYTES = 34

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

class PayloadType(Enum):
    TokenTransfer = 0x00
    SmartContract = 0x01
    VersionedSmartContract = 0x06
    ContractCall = 0x02
    PoisonMicroblock = 0x03
    Coinbase = 0x04
    CoinbaseToAltRecipient = 0x05


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
        "type": StacksMessageType.Address.value,
        "version": version,
        "hash160": hash
    }

def address_to_string(address):
    return c32_address(address["version"], address["hash160"]);

def get_stx_address(account, transaction_version = TransactionVersion.Testnet):
    return get_address_from_private_key(account.stx_private_key, transaction_version)


def make_stx_token_transfer(tx_options):
    if 'sender_key' in tx_options:
        public_key = pub_key_from_priv_key(tx_options["sender_key"])
        tx_options.pop("sender_key")
        tx_options["public_key"] = public_key
        transaction = make_unsigned_stx_token_transfer(tx_options)
        print(transaction)

def create_memo_string(memo_content):
    if len(memo_content.encode('utf-8')) > MEMO_MAX_LENGTH_BYTES:
        raise ValueError('Memo exceeds maximum length of '+MEMO_MAX_LENGTH_BYTES+' bytes')
    return { "type": StacksMessageType.MemoString.value, "content": memo_content };


def create_token_transfer_payload(recipient, amount, memo=None):
    recipient = prinicpal_cv(recipient)
    memo = create_memo_string(memo)
    print(recipient)
    print(memo)
    return {
        "type": StacksMessageType.Payload.value,
        "payloadType": PayloadType.TokenTransfer.value,
        "recipient": recipient,
        "amount": amount,
        "memo": memo or create_memo_string("")
    }

def estimate_transaction_byte_length(transaction):
    # TODO - SERIALIZE INTO BYTES AND RETUR LENGTH
    return 0

def estimate_transaction_fee_with_fallback(transaction, network):
    estimated_len = estimate_transaction_byte_length(transaction)
    # TODO - Continue from here.

def make_unsigned_stx_token_transfer(tx_options):
    options = {
        "fee": 0,
        "nonce": 0,
        "network": StacksMainnet(),
        "memo": "",
        "sponsored": False
    }

    options.update(tx_options)
    payload = create_token_transfer_payload(options["recipient"], options["amount"], options["memo"])
    print(payload)
    authorization = None
    spending_condition = None

    # TODO - Implement:
    if 'public_key' in options:
        pass
    else:
        pass

    # TODO - Implement
    if options["sponsored"]:
        pass
    else:
        pass

    # TODO - optionally get network from name
    network = options["network"]

    transaction = StacksTransaction(
        network.version.value, #value or enum?
        authorization,
        payload,
        None,
        None,
        options["anchor_mode"],
        network.chainId.value #value or enum
    )

    if ("fee" not in tx_options):
        fee = estimate_transaction_fee_with_fallback(transaction, network)