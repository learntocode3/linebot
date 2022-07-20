import mysql.connector
from mysql.connector import errorcode
import json
from model.settings import USER_TEST, PASSWORD

class linebotDB():
    def __init__(self):
        try:
            cnx = mysql.connector.connect(user=USER_TEST,
                                          password=PASSWORD,
                                          database='summerShredding')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("database connect success")
