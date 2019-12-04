from datetime import datetime
from typing import Any, Optional

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
        fountains: Collection = self.db.fountains
        buildings: Collection = self.db.buildings
        campuses: Collection = self.db.campuses

        users.create_index("UserName", unique=True)
        fountains.create_index("Name", unique=True)
        buildings.create_index("Name", unique=True)
        campuses.create_index("Name", unique=True)

    def add_user(
        self,
        user_name: str,
        first_name: str,
        last_name: str,
        password: str,
    ):
        """
        Creates a user with the given attributes.
        """
        users: Collection = self.db.users
        users.insert_one({
            "UserName": user_name,
            "FirstName": first_name,
            "LastName": last_name,
            "Password": password,
        })

    def login_user(
            self,
            user_name: str,
            password: str,
    ) -> Optional[str]:
        """
        Returns the user id if the username, password combination are correct;
        returns None otherwise.
        """
        users: Collection = self.db.users
        user = users.find_one({
            "UserName": user_name
        })

        if user is None:
            return None

        if user["Password"] != password:
            return None

        return str(user["_id"])

    def add_rating(
            self,
            score: int,
            timestamp: datetime,
            fountain_id: str,
            user_id: int,
    ):
        raise NotImplementedError()

    def get_average_rating(
            self,
            fountain_id: str,
    ) -> Optional[float]:
        raise NotImplementedError()

    def add_fountain(
            self,
            building_id: str,
            fountain_name: str,
    ):
        raise NotImplementedError()

    def lookup_fountain(
            self,
            fountain_name: str,
    ) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    def add_building(
            self,
            building_name: str,
            latitude: float,
            longitude: float,
            campus_id: str,
    ):
        raise NotImplementedError()

    def add_campus(
            self,
            city: str,
            state: str,
            campus_name: str,
    ):
        raise NotImplementedError()

    def get_campus_id(
            self,
            campus_name: str
    ) -> Optional[str]:
        raise NotImplementedError()

    def list_fountains(
            self,
            building_name: str,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    def list_buildings(
            self,
            campus_name: str,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()
