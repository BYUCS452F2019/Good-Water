import mysql.connector as mysql
import json

class DAO():
    def __init__(self):
        pass

    def connectToDatabase(self):
        credentials = json.load(open("credentials.json"))
        self.connection = mysql.connect(
            user=credentials['username'],
            password=credentials['password'],
            database=credentials['database'],
            host=credentials['host']
        )

    def disconnectFromDatabase(self):
        if self.connection:
            self.connection.close()

    def dropTables(self):
        statement = open("SQL_Statements/dropTables.txt").read()
        for result in self.connection.cmd_query_iter(statement):
            pass

    def createTables(self):
        statement = open("SQL_Statements/createTables.txt").read()
        for result in self.connection.cmd_query_iter(statement):
            pass


dao = DAO()
dao.connectToDatabase()
dao.dropTables()
dao.createTables()
dao.disconnectFromDatabase()
