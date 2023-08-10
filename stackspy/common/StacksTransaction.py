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
        pass

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
        pass

    def txid(self):
        pass

    def set_sponsor(self, sponsor_spending_condition):
        pass

    def set_fee(self, amount):
        pass

    def set_nonce(self, nonce):
        pass

    def set_sponsor_nonce(self, nonce):
        pass

    def serialize(self):
        pass
