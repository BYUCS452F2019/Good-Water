import mysql.connector as mysql
import json
import pandas as pd


class DAO():
    def __init__(self):
        self.connection = None

    def connect_to_database(self):
        credentials = json.load(open("./credentials.json"))
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
        statement = open("SQL_Statements/dropTables.txt").read()
        for result in self.connection.cmd_query_iter(statement):
            pass

    def create_tables(self):
        statement = open("SQL_Statements/createTables.txt").read()
        for result in self.connection.cmd_query_iter(statement):
            pass

    def add_user(self, user_name: str, first_name: str, last_name: str, password: str):
        cursor = self.connection.cursor()
        add_user = open("SQL_Statements/addUser.txt").read()

        user_info = {
            'user_name': user_name,
            'first_name': first_name,
            'last_name': last_name,
            'password': password
        }

        cursor.execute(add_user, user_info)
        self.connection.commit()
        cursor.close()

    def add_rating(self, score: int, dateT: str, fountain_id: int, user_id: int):
        cursor = self.connection.cursor()
        add_rating = open("SQL_Statements/addRating.txt").read()

        rating_info = {
            'score': score,
            'dateT': dateT,
            'fountain_id': fountain_id,
            'user_id': user_id
        }

        cursor.execute(add_rating, rating_info)
        self.connection.commit()
        cursor.close()

    def add_fountain(self, building_id: str, fountain_name: str):
        cursor = self.connection.cursor()
        add_fountain = open("SQL_Statements/addFountain.txt").read()

        fountain_info = {
            'building_id': building_id,
            'fountain_name': fountain_name
        }

        cursor.execute(add_fountain, fountain_info)
        self.connection.commit()
        cursor.close()

    def add_building(self, building_name: str, latitude: float, longitude: float, campus_id: int):
        cursor = self.connection.cursor()
        add_building = open("SQL_Statements/addBuilding.txt").read()

        building_info = {
            'building_name': building_name,
            'latitude': latitude,
            'longitude': longitude,
            'campus_id': campus_id
        }

        cursor.execute(add_building, building_info)
        self.connection.commit()
        cursor.close()

    def add_campus(self, city: str, state: str, campus_name: str):
        cursor = self.connection.cursor()
        add_campus = open("SQL_Statements/addCampus.txt").read()

        campus_info = {
            'city': city,
            'state': state,
            'campus_name': campus_name
        }

        cursor.execute(add_campus, campus_info)
        self.connection.commit()
        cursor.close()

if __name__ == "__main__":
    dao = DAO()
    dao.connect_to_database()
    dao.drop_tables()
    dao.create_tables()
    dao.add_user('paj', 'Paul', 'Johnston', '123')
    dao.add_campus('Provo', 'Utah', 'BYU-Provo')

    myDF = pd.read_csv("Building_Coordinates.csv", sep=',')
    # print(myDF)

    for i in range(0, len(myDF.index)):
        dao.addBuilding(myDF['Name'][i], myDF['Latitude'][i], myDF['Longitude'][i], 0)

    dao.disconnect_from_database()
