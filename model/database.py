import mysql.connector
from mysql.connector import errorcode
import json
from settings import USER_TEST, PASSWORD

# print(USER,PASSWORD)

# connect to mysql
DB_NAME = 'linebot'
cnx = mysql.connector.connect(user=USER_TEST,
                              password=PASSWORD,
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()

# Create datebase if not exist
def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

cnx = mysql.connector.connect(user=USER_TEST,
                              password=PASSWORD,
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()
cursor.execute("USE {}".format(DB_NAME))
TABLES = {}
TABLES['member'] = (
    "CREATE TABLE `member` ("
    "  `user_id` VARCHAR(255) NOT NULL,"
    "  `image_id` VARCHAR(255) NOT NULL"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


