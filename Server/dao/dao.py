import mysql.connector as mysql
import json


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
        if self.connection is None:
            self.connectToDatabase()

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
        self.connection.close()


    def add_rating(self):
        pass

    def add_fountain(self):
        pass

    def add_building(self):
        pass

    def add_campus(self):
        pass


dao = DAO()
dao.connect_to_database()
dao.drop_tables()
dao.create_tables()
dao.add_user('paj', 'Paul', 'Johnston', '123')
dao.disconnect_from_database()
