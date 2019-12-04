from authenticator import Authenticator
from dao.basedao import BaseDAO


class ServerContext:
    authenticator: Authenticator
    dao: BaseDAO

    def __init__(
            self,
            authenticator: Authenticator,
            dao: BaseDAO,
    ):
        self.dao = dao
        self.authenticator = authenticator
