from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
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

    def _get_document_id(
            self,
            collection: Collection,
            params: Dict[str, Any],
    ) -> Optional[str]:
        doc = collection.find_one(params)
        return str(doc["_id"]) if doc is not None else None

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

        users.create_index("userName", unique=True)
        fountains.create_index("name", unique=True)
        fountains.create_index("buildingID")
        buildings.create_index("name", unique=True)
        campuses.create_index("name", unique=True)

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
            "userName": user_name,
            "firstName": first_name,
            "lastName": last_name,
            "password": password,
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
            "userName": user_name
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
        fountains: Collection = self.db.fountains
        fountains.insert_one({
            "name": fountain_name,
            "buildingID": ObjectId(building_id),
        })

    def lookup_fountain(
            self,
            fountain_name: str,
    ) -> Optional[Dict[str, Any]]:
        fountains: Collection = self.db.fountains
        fountain = fountains.find_one({
            "name": fountain_name,
        })

        if fountain is None:
            return None

        return str(fountain["_id"])

    def add_building(
            self,
            building_name: str,
            latitude: float,
            longitude: float,
            campus_id: str,
    ):
        buildings: Collection = self.db.buildings
        buildings.insert_one({
            "name": building_name,
            "latitude": latitude,
            "longitude": longitude,
            "campus_id": ObjectId(campus_id),
        })

    def add_campus(
            self,
            city: str,
            state: str,
            campus_name: str,
    ):
        campuses: Collection = self.db.campuses
        campuses.insert_one({
            "name": campus_name,
            "city": city,
            "state": state,
        })

    def get_campus_id(
            self,
            campus_name: str
    ) -> Optional[str]:
        return self._get_document_id(
            self.db.campuses,
            {"name": campus_name},
        )

    def list_fountains(
            self,
            building_name: str,
    ) -> List[Dict[str, Any]]:
        building_id = self._get_document_id(
            self.db.buildings,
            {"name": building_name},
        )

        if building_id is None:
            # TOOD: should this be an error?
            return []

        fountains: Collection = self.db.fountains
        fountain_docs = fountains.find({
            "buildingID": ObjectId(building_id),
        })

        return [
            {
                "id": str(f["_id"]),
                "name": f["name"],
            }
            for f in fountain_docs
        ]

    def list_buildings(
            self,
            campus_name: str,
    ) -> List[Dict[str, Any]]:
        campus_id = self._get_document_id(
            self.db.campuses,
            {"name": campus_name},
        )

        if campus_id is None:
            # TODO: should this be an error?
            return []

        buildings: Collection = self.db.buildings
        building_docs = buildings.find({
            "campusID": ObjectId(campus_id),
        })

        return [
            {
                "id": str(b["_id"]),
                "name": b["name"],
                "latitude": b["latitude"],
                "longitude": b["longitude"],
            }
            for b in building_docs
        ]
