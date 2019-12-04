from pymongo import MongoClient
from pymongo.database import Collection, Database


class MongoDAO:
    host: str
    port: int
    db_name: str

    client: MongoClient
    db: Database

    def __init__(self, host: str, port: int, db_name: str):
        self.host = host
        self.port = port
        self.db_name = db_name

    def connect_to_database(self):
        self.client = MongoClient(
            host=self.host,
            port=self.port,
        )
        self.db = self.client[self.db_name]

    def drop_tables(self):
        self.client.drop_database(self.db_name)
        self.db = self.client[self.db_name]
    
    def create_tables(self):
        users: Collection = self.db.users
        users.create_index("UserName", unique=True)

    def add_user(self, user_name: str, first_name: str, last_name: str, password: str):
        users: Collection = self.db.users
        users.insert_one({
            "UserName": user_name,
            "FirstName": first_name,
            "LastName": last_name,
            "Password": password,
        })

