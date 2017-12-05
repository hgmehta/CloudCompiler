import mysql.connector
from mysql.connector import Error
import datetime

def createConnection():
    try:
        return mysql.connector.connect(host='localhost', port='3306', database='cloudcompiler', user='root', password='lab@cc2')
    except Error as error:
        print("Sorry, Some problem in making connection with database")
