import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'DaveSon#!35@'
)

#prepare a cursor object
cursorObject = dataBase.cursor()

#create a database

cursorObject.execute("CREATE DATABASE davedb")

print("All Done!")