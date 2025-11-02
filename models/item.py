import time

class Item:
    def __init__(self, payload: bytes, created_at: float, expiration: float|None, should_burn: bool, paste_bin_url= "", password=None):
        self.payload = payload
        self.created_at = created_at
        self.expiration = expiration
        self.should_burn = should_burn
        self.password: str|None = password
        self.paste_bin_url = paste_bin_url

    def is_expired(self):
        return self.expiration is not None and (self.expiration <= time.time())