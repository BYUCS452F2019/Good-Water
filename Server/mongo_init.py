import json

from init_db import init_db
from dao.mongodao import MongoDAO
from utils import relative


def mongo_init():
    config = json.load(
        open(relative(__file__, "config/mongoconfig.json"))
    )
    dao = MongoDAO(
        host=config["host"],
        port=config["port"],
        db_name=config["dbName"],
    )
    init_db(dao)


if __name__ == "__main__":
    mongo_init()
