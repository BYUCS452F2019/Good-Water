from authenticator import Authenticator
from dao.dao import DAO


class ServerContext:
    authenticator: Authenticator
    dao: DAO

    def __init__(
            self,
            authenticator: Authenticator,
            dao: DAO,
    ):
        self.dao = dao
        self.authenticator = authenticator
