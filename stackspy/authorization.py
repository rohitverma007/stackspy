from typing import Dict
import copy
from common.helpers import sha512_256
from encryption import sign_with_key
from constants import RECOVERABLE_ECDSA_SIG_LENGTH_BYTES, AuthType
from common.helpers import is_hex_addy_compressed, left_pad_hex, is_single_sig, empty_signature_message, create_standard_auth
from common.helpers import pub_key_from_priv_key

def make_sig_hash_pre_sign(cur_sig_hash, auth_type, fee, nonce):
    # new hash combines the previous hash and all the new data this signature will add. This
    # includes:
    # * the previous hash
    # * the auth flag
    # * the tx fee (big-endian 8-byte number)
    # * nonce (big-endian 8-byte number)
    hash_length = 32 + 1 + 8 + 8    
    sig_hash = cur_sig_hash + auth_type.to_bytes(1, 'big').hex() + fee.to_bytes(8, 'big').hex() + nonce.to_bytes(8, 'big').hex()
    if len(bytearray.fromhex(sig_hash)) != hash_length:
        raise ValueError('Invalid signature hash length')
    return sha512_256(bytearray.fromhex(sig_hash))


def make_sig_hash_post_sign(cur_sig_hash: str, pub_key: str, signature: str) -> str:
    """
    Create a signature hash after signing.
    :param cur_sig_hash: Current signature hash as a string.
    :param pub_key: Public key as a string.
    :param signature: Message signature as a string.
    :return: Signature hash as a string.
    """
    # new hash combines the previous hash and all the new data this signature will add.  This
    # includes:
    # * the public key compression flag
    # * the signature
    hash_length = 32 + 1 + RECOVERABLE_ECDSA_SIG_LENGTH_BYTES

    pub_key_encoding = 1 if is_hex_addy_compressed(pub_key) else 0  # Assuming 1: Compressed, 0: Uncompressed

    sig_hash = cur_sig_hash + left_pad_hex(hex(pub_key_encoding)[2:]) + signature

    if len(bytearray.fromhex(sig_hash)) > hash_length:
        raise ValueError('Invalid signature hash length')

    return sha512_256(bytearray.fromhex(sig_hash))

def next_signature(cur_sig_hash: str, auth_type: str, fee: int, nonce: int, private_key: str) -> Dict[str, str]:
    sig_hash_pre_sign = make_sig_hash_pre_sign(cur_sig_hash, auth_type, fee, nonce) #this works lets fucking go.
    signature = sign_with_key(sig_hash_pre_sign.hex(), private_key["data"])
    public_key = pub_key_from_priv_key(private_key["data"])
    next_sig_hash = make_sig_hash_post_sign(sig_hash_pre_sign.hex(), public_key, signature["data"])
    return {
        'nextSig': signature,
        'nextSigHash': next_sig_hash.hex()
    }

def clear_condition(spending_condition):
    cloned_condition =  copy.deepcopy(spending_condition)
    cloned_condition["nonce"] = 0
    cloned_condition["fee"] = 0

    if is_single_sig(cloned_condition):
        cloned_condition["signature"] = empty_signature_message()
    else:
        # no single TODO
        cloned_condition["fields"] = []

    return cloned_condition

def into_initial_sighash_auth(auth):
    """
    Convert the given authorization into its initial sighash form.
    :param auth: The Authorization object.
    :return: The Authorization in its initial sighash form.
    """
    if auth["spendingCondition"]:
        if auth["authType"] == AuthType.Standard:
            return create_standard_auth(clear_condition(auth["spendingCondition"]))
        elif auth["authTyp"] == AuthType.Sponsored:
            pass
        else:
            raise ValueError('Unexpected authorization type for signing')
    
    raise ValueError('Authorization missing SpendingCondition')

