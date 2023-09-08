import copy
from constants import AuthType
from authorization import next_signature, into_initial_sighash_auth
from .clarity import serialize_cv
from .helpers import PayloadType, serialize_memo_string, is_single_sig, sha512_256

class StacksTransaction:
    def __init__(self, version, auth, payload, post_conditions=None, post_condition_mode=None, anchor_mode=None, chain_id=None):
        self.version = version
        self.auth = auth
        self.payload = payload
        self.chain_id = chain_id
        self.post_condition_mode = post_condition_mode
        self.post_conditions = post_conditions
        self.anchor_mode = anchor_mode

    def sign_begin(self):
        tx = copy.deepcopy(self)
        tx.auth = into_initial_sighash_auth(tx.auth)
        return tx.txid()

    def sign_next_origin(self, sig_hash, priv_key):
        if not self.auth["spendingCondition"]:
            # error
            pass

        if not self.auth["authType"]:
            # error
            pass

        return self.sign_and_append(self.auth["spendingCondition"], sig_hash, AuthType.Standard, priv_key)

    def verify_being(self):
        pass

    def verify_origin(self):
        pass

    def sign_nex_origin(self, sig_hash, private_key):
        pass

    def sign_next_sponsor(self, sig_hash, private_key):
        pass

    def append_pub_key(self, public_key):
        pass

    def sign_and_append(self, condition, cursig_hash, auth_type, private_key):
        next_sig_data = next_signature(
            cursig_hash, auth_type.value, self.auth["spendingCondition"]["fee"], self.auth["spendingCondition"]["nonce"], private_key
        )
        if is_single_sig(condition):
            self.auth["spendingCondition"]["signature"] = next_sig_data["nextSig"]
        return next_sig_data["nextSigHash"]

    def txid(self):
        serialized = self.serialize();
        return sha512_256(serialized).hex()

    def set_sponsor(self, sponsor_spending_condition):
        pass

    def set_fee(self, amount):
        if self.auth["authType"] == AuthType.Standard:
            self.auth["spendingCondition"]["fee"] = amount
        elif self.auth["authType"] == AuthType.Sponsored:
            # TODO implement
            pass



    def set_nonce(self, nonce):
        if self.auth["authType"] == AuthType.Standard:
            self.auth["spendingCondition"]["nonce"] = nonce
        elif self.auth["authType"] == AuthType.Sponsored:
            # TODO implement
            pass

    def set_sponsor_nonce(self, nonce):
        pass

    def serialize_payload(self):
        payload_bytes_array = bytearray()
        payload_bytes_array.append(self.payload["payloadType"])

        if self.payload["payloadType"] == PayloadType.TokenTransfer.value:
            payload_bytes_array += serialize_cv(self.payload["recipient"])
            payload_bytes_array += self.payload["amount"].to_bytes(8, 'big')
            payload_bytes_array += serialize_memo_string(self.payload["memo"])

        return payload_bytes_array
        # TODO - implement other payload types

    def serialize_single_sig_spending_condition(self, spending_condition):
        bytes_array = bytearray()
        bytes_array.append(spending_condition["hashMode"].value)
        bytes_array += bytearray(bytes.fromhex(spending_condition["signer"]["hash160"]))
        bytes_array += spending_condition["nonce"].to_bytes(8, 'big')
        bytes_array += spending_condition["fee"].to_bytes(8, 'big')
        bytes_array.append(spending_condition["keyEncoding"].value)
        bytes_array += bytearray(bytes.fromhex(spending_condition["signature"]["data"]))
        return bytes_array
        
    def serialize_spending_condition(self):
        spending_condition = self.auth["spendingCondition"]
        bytes_array = bytearray()
        if is_single_sig(spending_condition):
            bytes_array += self.serialize_single_sig_spending_condition(spending_condition)
        else:
            # TODO MultiSig
            pass
        return bytes_array

    def serialize_authorization(self):
        bytes_array = bytearray()
        bytes_array.append(self.auth["authType"].value)
        if self.auth["authType"] == AuthType.Standard:
            bytes_array += self.serialize_spending_condition()
        elif self.auth["authType"] == AuthType.Sponsored:
            # TODO implement
            pass
        return bytes_array

    def serialize(self):
        if self.version is None:
            raise ValueError('version is undefined')
        
        if self.chain_id is None:
            raise ValueError('chain_id is undefined')

        # Can be undefined for single sig with sender key?
        # if not self.auth:
        #     raise ValueError('auth is undefined')

        # Can be undefined for single sig with sender key?
        # if not self.anchor_mode:
        #     raise ValueError('anchor_mode is undefined')                                    

        if self.payload is None:
            raise ValueError('payload is undefined')

        bytes_array = bytearray()
        bytes_array.append(self.version)
        bytes_array += self.chain_id.to_bytes(4, 'big')
        bytes_array += self.serialize_authorization()
        bytes_array += bytearray(bytes.fromhex("03")) #HARD CODING anchor mode
        bytes_array += bytearray(bytes.fromhex("02")) #HARD CODING postcondition mode
        length_of_pc = 0
        bytes_array += length_of_pc.to_bytes(4, 'big') #HARD CODING postconditons list
        bytes_array += self.serialize_payload()

        return bytes_array