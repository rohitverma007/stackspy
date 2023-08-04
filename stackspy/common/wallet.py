from typing import List

class Account:
    # Add attributes for the Account class here.
    pass

class Wallet:
    def __init__(self, salt: str, root_key: str, config_private_key: str, encrypted_secret_key: str,
                 accounts: List[Account]):
        self.salt = salt
        self.root_key = root_key
        self.config_private_key = config_private_key
        self.encrypted_secret_key = encrypted_secret_key
        self.accounts = accounts 

