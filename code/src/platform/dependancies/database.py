import mysql.connector
from mysql.connector import Error
import datetime

def createConnection():
    return mysql.connector.connect(host='localhost', port='3306', database='cloudcompiler', user='root', password='lab@cc2')
