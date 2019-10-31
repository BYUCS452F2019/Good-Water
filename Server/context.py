from dao.dao import DAO


class ServerContext:
    dao: DAO

    def __init__(
            self,
            dao: DAO,
    ):
        self.dao = dao
