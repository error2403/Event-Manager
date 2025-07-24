import mysql.connector
from mysql.connector import errorcode
import mysql.connector.cursor

import os
from dotenv import load_dotenv

load_dotenv()

# create config for mysql server connection
config = {
    'user': os.getenv("USER"),
    'password': os.getenv("PASSWORD"),
    'host': os.getenv("HOST"),
    'database': ''      # database left empty so we can create it if it doesnt exist
}

# try to create connection to mysql server
try:
    # ** is used to unpack a dictionary (grab all the key-value pairs out of it)
      # * is used to unpack a list/tuple (grab all the values out of it)
    cnx = mysql.connector.connect(**config)
    print("connection successful")

# catch any errors thrown during connection
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("user name or password is incorrect.")
        exit(101)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
        exit(102)
    else:
        print("unknown connection error: " + err)
        exit(103)

# no errors in mysql server connection, good to proceed
# create cursor to execute mysql commands
cursor = cnx.cursor()

def create_database(cursor: mysql.connector.cursor.MySQLCursor, db_name: str):
    """Create database for given cursor connection and name.

    Args:
        cursor: cursor to the mysql server.
        db_name: name of the database to create.
    
    Returns:
        nothing.
    """

    cursor.execute(
        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name)
    )


# try to switch to test database
DB_NAME = 'test_database'
try:
    cursor.execute("USE {}".format(DB_NAME))

# catch any errors thrown during database switch
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database {} does not exist.".format(DB_NAME))
        create_database(cursor, DB_NAME)
        exit(102)
    else:
        print("unknown DB error: " + err)
        exit(103)


# try to create table
cnx.close()