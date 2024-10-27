import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456789",
    auth_plugin='mysql_native_password')

mycursor = mydb.cursor("CREATE DATABASE users_db")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)    