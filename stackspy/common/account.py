from typing import Optional

class Profile:
    # TODO - Implement
    pass

class Account:
    def __init__(
        self,
        stx_private_key: str,
        data_private_key: str,
        salt: str,
        apps_key: str,
        index: int,
        username: Optional[str] = None,
        profile: Optional[Profile] = None
    ):
        self.stx_private_key = stx_private_key
        self.data_private_key = data_private_key
        self.salt = salt
        self.apps_key = apps_key
        self.index = index
        self.username = username
        self.profile = profile