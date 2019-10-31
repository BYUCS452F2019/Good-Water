import random
from typing import Dict, Optional

from dao.dao import DAO


class Authenticator:
    token_map: Dict[str, str]
    dao: DAO

    def __init__(self, dao: DAO):
        self.token_map = {}
        self.dao = dao

    def create_token(self, username: str, password: str) -> Optional[str]:
        # TODO: use self.dao to check the username and password against the DB
        # this should return NONE if the username/pass combo does not exist
        # this should also look up the user ID
        # for now this just uses "abc" for the user ID
        user_id = "abc"
        token = f"{random.randint(0xFFFFFFFFFFFFFFFF):016x}"

        while token in self.token_map:
            token = f"{random.randint(0xFFFFFFFFFFFFFFFF):016x}"

        self.token_map[token] = user_id
        return token

    def lookup_token(self, token: str) -> Optional[str]:
        if token in self.token_map:
            return self.token_map[token]
        else:
            return None
