# import mysql.connector

# def get_connection():
#     connection = mysql.connector.connect(
#         host = "localhost",
#         user = "root",
#         password ="1",
#         database ="diarydb"
#     )
    
#     return connection

import mysql.connector
import os

def get_connection():
    connection = mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=int(os.environ.get("MYSQLPORT", 3306))
    )
    return connection