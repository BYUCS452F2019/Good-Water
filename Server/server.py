import mysql.connector as mysql
import json

class Server():
    def __init__(self):
        pass

    #This class is responsible for making API endpoints that
    # will receive JSON objects and then call DAO methods such as "addUser"
    # "addBuildling" etc.
