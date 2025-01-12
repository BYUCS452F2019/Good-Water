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
        user_id = self.dao.login_user(
            user_name=username,
            password=password,
        )

        if user_id is None:
            return None

        token = f"{random.randint(0, 0xFFFFFFFFFFFFFFFF):016x}"

        while token in self.token_map:
            token = f"{random.randint(0, 0xFFFFFFFFFFFFFFFF):016x}"

        self.token_map[token] = user_id
        return token

    def lookup_token(self, token: Optional[str]) -> Optional[int]:
        if token in self.token_map:
            return self.token_map[token]
        else:
            return None
