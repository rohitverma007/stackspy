import json
import requests
from network import StacksNetwork
from enum import Enum
import hashlib
from common.c32helpers import c32_address
from common.helpers import StacksMessageType, PayloadType, pub_key_from_priv_key, empty_signature_message, create_standard_auth
from common.clarity import prinicpal_cv
from network import StacksTestnet
from common.StacksTransaction import StacksTransaction
from constants import TransactionVersion, PubKeyEncoding
from common.TransactionSigner import TransactionSigner

MEMO_MAX_LENGTH_BYTES = 34
PRIVATE_KEY_COMPRESSED_LENGTH  = 33

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


def get_address_from_private_key(private_key, transaction_version):
    pub_key = pub_key_from_priv_key(private_key)
    return get_address_from_public_key(pub_key, transaction_version)


def get_address_from_public_key(pub_key, transaction_version):
    address_version = address_hash_mode_to_version(AddressHashMode.SerializeP2PKH, transaction_version)
    address_dict = address_from_version_hash(address_version, hashlib.new('ripemd160', hashlib.sha256(bytearray.fromhex(pub_key)).digest()).hexdigest())
    address_string = address_to_string(address_dict)
    return address_string



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
        priv_key_address = tx_options["sender_key"]
        tx_options.pop("sender_key")
        tx_options["public_key"] = public_key
        transaction = make_unsigned_stx_token_transfer(tx_options)
        priv_key = {
            "data": priv_key_address,
            "compressed": len(bytearray.fromhex(priv_key_address)) == PRIVATE_KEY_COMPRESSED_LENGTH
        }
        signer = TransactionSigner(transaction)
        signer.sign_origin(priv_key)
        return transaction

def create_memo_string(memo_content):
    if len(memo_content.encode('utf-8')) > MEMO_MAX_LENGTH_BYTES:
        raise ValueError('Memo exceeds maximum length of '+MEMO_MAX_LENGTH_BYTES+' bytes')
    return { "type": StacksMessageType.MemoString.value, "content": memo_content };


def create_token_transfer_payload(recipient, amount, memo=None):
    recipient = prinicpal_cv(recipient)
    memo = create_memo_string(memo)
    return {
        "type": StacksMessageType.Payload.value,
        "payloadType": PayloadType.TokenTransfer.value,
        "recipient": recipient,
        "amount": amount,
        "memo": memo or create_memo_string("")
    }

def estimate_transaction_byte_length(transaction):
    # TODO - implement multi-sig
    return len(transaction.serialize())

def get_nonce(sender_address, network):
    derived_network = StacksNetwork.fromNameOrNetwork(network)
    response = requests.get(derived_network.getAccountApiUrl(sender_address))
    return response.json()["nonce"]

def estimate_transaction_fee_with_fallback(transaction, network):
    estimated_len = estimate_transaction_byte_length(transaction)
    fee_estimation = estimate_transaction(transaction, estimated_len, network)
    return fee_estimation
    # TODO - fallback?

def get_address_dict_from_pub_key(public_key, transaction_version):
    address_version = address_hash_mode_to_version(AddressHashMode.SerializeP2PKH, transaction_version)
    address_dict = address_from_version_hash(address_version, hashlib.new('ripemd160', hashlib.sha256(bytearray.fromhex(public_key)).digest()).hexdigest())
    return address_dict

def create_single_sig_spending_condition(hash_mode, public_key, nonce, fee, transaction_version=TransactionVersion.Testnet):
    signer = get_address_dict_from_pub_key(public_key, transaction_version)
    key_encoding = PubKeyEncoding.Compressed
    return {
        "hashMode": hash_mode,
        "signer": signer,
        "nonce": nonce,
        "fee": fee,
        "keyEncoding": key_encoding,
        "signature": empty_signature_message()
    }
        

def make_unsigned_stx_token_transfer(tx_options):
    options = {
        "fee": 0,
        "nonce": 0,
        "network": StacksTestnet(),
        "memo": "",
        "sponsored": False
    }

    options.update(tx_options)
    payload = create_token_transfer_payload(options["recipient"], options["amount"], options["memo"])
    authorization = None
    spending_condition = None

    if 'public_key' in options:
        spending_condition = create_single_sig_spending_condition(
            AddressHashMode.SerializeP2PKH,
            options["public_key"],
            options["nonce"],
            options["fee"],
            options["network"].version
        )
    else:
        pass

    # TODO - Implement
    if options["sponsored"]:
        pass
    else:
        authorization = create_standard_auth(spending_condition)

    # TODO - optionally get network from name
    network = options["network"]

    transaction = StacksTransaction(
        network.version.value, #value or enum?
        authorization,
        payload,
        None,
        None,
        None,
        network.chainId.value #value or enum
    )

    if ("fee" not in tx_options):
        fee = estimate_transaction_fee_with_fallback(transaction, network)
        transaction.set_fee(fee)
    else:
        transaction.set_fee(tx_options["fee"])
    
    if ("nonce" not in tx_options):
        address_version = AddressVersion.TestnetSingleSig
        if network.version == TransactionVersion.Mainnet:
            address_version = AddressVersion.MainnetSingleSig
        sender_address = c32_address(address_version, transaction.auth["spendingCondition"]["signer"]["hash160"])
        tx_nonce = get_nonce(sender_address, network)
        transaction.set_nonce(tx_nonce)
    else:
        transaction.set_nonce(tx_options["nonce"])
    return transaction

def broadcast_transaction(transaction, network, attachment=None):
    raw_tx = transaction.serialize()
    derived_network = StacksNetwork.fromNameOrNetwork(network)
    response = requests.post(derived_network.getBroadcastApiUrl(), headers={'Content-Type': 'application/octet-stream'}, data=raw_tx)
    return response

def estimate_transaction(transaction, estimated_len=None, network=None):
    derived_network = StacksNetwork.fromNameOrNetwork(network)
    response = requests.post(derived_network.getTransactionFeeEstimateApiUrl(), headers={'Content-Type': 'application/json'}, data=json.dumps({
        "transaction_payload": transaction.serialize_payload().hex(),
        "estimated_len": estimated_len # TODO - optionally dont send
    }))
    return response.json()["estimations"][1]["fee"]