import json
import os
import mysql.connector as mysql
import pandas as pd

from datetime import datetime
from typing import Any, Dict, List, Optional


def relative(path: str) -> str:
    """find the path relative to the current file rather than the cwd"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, path)


class DAO():
    def __init__(self):
        self.connection = None

    def connect_to_database(self):
        credentials = json.load(open(relative("credentials.json")))
        self.connection = mysql.connect(
            user=credentials['username'],
            password=credentials['password'],
            database=credentials['database'],
            host=credentials['host']
        )

    def disconnect_from_database(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def drop_tables(self):
        statement = open(relative("SQL_Statements/dropTables.txt")).read()
        for result in self.connection.cmd_query_iter(statement):
            pass

    def create_tables(self):
        statement = open(relative("SQL_Statements/createTables.txt")).read()
        for result in self.connection.cmd_query_iter(statement):
            pass

    def add_user(self, user_name: str, first_name: str, last_name: str, password: str):
        cursor = self.connection.cursor()
        add_user = open(relative("SQL_Statements/addUser.txt")).read()

        user_info = {
            'user_name': user_name,
            'first_name': first_name,
            'last_name': last_name,
            'password': password
        }

        cursor.execute(add_user, user_info)
        self.connection.commit()
        cursor.close()

    def login_user(self, user_name: str, password: str) -> Optional[int]:
        cursor = self.connection.cursor()
        login_user = open(relative("SQL_Statements/loginUser.txt")).read()

        login_info = {
            "user_name": user_name,
            "password": password,
        }

        cursor.execute(login_user, login_info)
        results = list(cursor)
        assert len(results) <= 1

        if len(results) == 0:
            user_id = None
        else:
            user_id = results[0][0]

        self.connection.commit()
        cursor.close()
        return user_id

    def add_rating(self, score: int, timestamp: datetime, fountain_id: str, user_id: str):
        cursor = self.connection.cursor()
        add_rating = open(relative("SQL_Statements/addRating.txt")).read()

        rating_info = {
            'score': score,
            'dateT': timestamp,
            'fountain_id': fountain_id,
            'user_id': user_id
        }

        cursor.execute(add_rating, rating_info)
        self.connection.commit()
        cursor.close()

    def get_average_rating(self, fountain_id: int) -> Optional[float]:
        cursor = self.connection.cursor()
        add_fountain = open(
            relative("SQL_Statements/getAverageRating.txt")).read()

        rating_info = {
            'fountain_id': fountain_id
        }

        cursor.execute(add_fountain, rating_info)

        results = list(cursor)
        assert len(results) <= 1

        if len(results) == 0:
            value = None
        else:
            value = results[0][0]

        self.connection.commit()
        cursor.close()
        return value

    def add_fountain(self, building_id: str, fountain_name: str):
        cursor = self.connection.cursor()
        add_fountain = open(relative("SQL_Statements/addFountain.txt")).read()

        fountain_info = {
            'building_id': building_id,
            'fountain_name': fountain_name
        }
        cursor.execute(add_fountain, fountain_info)
        self.connection.commit()
        cursor.close()

    def lookup_fountain(self, fountain_name: str) -> Optional[Dict[str, Any]]:
        cursor = self.connection.cursor()
        lookup_fountain = open(
            relative("SQL_Statements/lookupFountain.txt")).read()

        fountain_info = {
            'fountain_name': fountain_name
        }

        cursor.execute(lookup_fountain, fountain_info)

        results = list(cursor)
        assert len(results) <= 1

        if len(results) == 0:
            fountain = None
        else:
            fountain_id, fountain_name = results[0]
            fountain = {
                "id": fountain_id,
                "name": fountain_name,
            }

        self.connection.commit()
        cursor.close()
        return fountain

    def add_building(self, building_name: str, latitude: float, longitude: float, campus_id: int):
        cursor = self.connection.cursor()
        add_building = open(relative("SQL_Statements/addBuilding.txt")).read()

        building_info = {
            'building_name': building_name,
            'latitude': float(latitude),
            'longitude': float(longitude),
            'campus_id': campus_id
        }

        cursor.execute(add_building, building_info)
        self.connection.commit()
        cursor.close()

    def add_campus(self, city: str, state: str, campus_name: str):
        cursor = self.connection.cursor()
        add_campus = open(relative("SQL_Statements/addCampus.txt")).read()

        campus_info = {
            'city': city,
            'state': state,
            'campus_name': campus_name
        }

        cursor.execute(add_campus, campus_info)
        self.connection.commit()
        cursor.close()

    def get_campus_id(self, campus_name: str) -> int:
        cursor = self.connection.cursor()
        add_campus = open(relative("SQL_Statements/getCampusID.txt")).read()

        campus_info = {
            'campus_name': campus_name
        }

        cursor.execute(add_campus, campus_info)

        ids = list(cursor)
        self.connection.commit()
        cursor.close()
        return ids[0][0]

    def get_building_id(self, building_name: str) -> Optional[str]:
        cursor = self.connection.cursor()

        get_building_id = open(relative("SQL_Statements/getBuildingID.txt")).read()

        building_info = {
            'building_name': building_name
        }

        cursor.execute(get_building_id, building_info)

        ids = list(cursor)
        self.connection.commit()
        cursor.close()

        return ids[0][0]

    def get_user_id(self, user_name: str) -> Optional[str]:
        cursor = self.connection.cursor()

        get_user_id = open(relative("SQL_Statements/getUserID.txt")).read()

        user_info = {
            'user_name': user_name
        }

        cursor.execute(get_user_id, user_info)

        ids = list(cursor)
        self.connection.commit()
        cursor.close()
        return ids[0][0]

    def list_fountains(self, building_name: str) -> List[Dict[str, Any]]:
        cursor = self.connection.cursor()
        list_fountains = open(
            relative("SQL_Statements/listFountains.txt"),
        ).read()

        list_info = {
            "building_name": building_name,
        }

        cursor.execute(list_fountains, list_info)
        results = list(cursor)

        fountains = []

        for fountain_id, fountain_name in results:
            fountains.append({
                "id": fountain_id,
                "name": fountain_name,
            })

        self.connection.commit()
        cursor.close()
        return fountains

    def list_buildings(self, campus_name: str) -> List[Dict[str, Any]]:
        cursor = self.connection.cursor()

        list_buildings = open(
            relative("SQL_Statements/listBuildings.txt"),
        ).read()

        list_buildings_info = {
            "campus_id": self.get_campus_id(campus_name)
        }

        cursor.execute(list_buildings, list_buildings_info)
        results = list(cursor)

        buildings = []

        for (
            building_id,
            building_name,
            latitude,
            longitude,
        ) in results:
            buildings.append({
                "id": building_id,
                "name": building_name,
                "latitude": latitude,
                "longitude": longitude,
            })

        self.connection.commit()
        cursor.close()
        return buildings

    def list_campuses(self) -> List[Dict[str, Any]]:
        cursor = self.connection.cursor()
        list_campuses = open(
            relative("SQL_Statements/listCampuses.txt"),
        ).read()

        cursor.execute(list_campuses, {})
        results = list(cursor)

        campuses = []

        for (
            campus_id,
            campus_name,
            city,
            state,
        ) in results:
            campuses.append({
                "id": campus_id,
                "name": campus_name,
                "city": city,
                "state": state,
            })

        self.connection.commit()
        cursor.close()
        return campuses


def load_server():
    dao = DAO()
    dao.connect_to_database()
    dao.drop_tables()
    dao.create_tables()
    dao.add_user('paj', 'Paul', 'Johnston', '123')
    dao.add_campus('Provo', 'Utah', 'BYU-Provo')
    campus_id = dao.get_campus_id('BYU-Provo')

    myDF = pd.read_csv(relative("../Building_Coordinates.csv"), sep=',')

    for i in range(0, len(myDF.index)):
        dao.add_building(
            myDF['Name'][i],
            float(myDF['Latitude'][i]),
            float(myDF['Longitude'][i]),
            campus_id,
        )

    fountainData = pd.read_csv(relative("../FountainInput.csv"), sep=',')

    for i in range(0, len(fountainData.index)):
        dao.add_fountain(
            str(fountainData['Building_ID'][i]),
            str(fountainData['Fountain_Name'][i]),
        )

    ratingData = pd.read_csv(relative("../ratingInput.csv"), sep=',')

    for i in range(0, len(ratingData.index)):
        dao.add_rating(
            int(ratingData['Score'][i]),
            str(ratingData['Date'][i]),
            int(ratingData['Fountain_ID'][i]),
            int(ratingData['User_ID'][i]),
        )

    dao.disconnect_from_database()


# HERE'S WHERE YOU CAN CALL LOAD_SERVER TO FILL DATABASE
if __name__ == "__main__":
    load_server()
