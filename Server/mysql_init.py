from init_db import init_db
from dao.dao import DAO


def mysql_init():
    dao = DAO()
    init_db(dao)


if __name__ == "__main__":
    mysql_init()
