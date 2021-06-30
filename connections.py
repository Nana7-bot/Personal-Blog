import mysql.connector

myDb = mysql.connector.connect(
    host='localhost',
    user='proviea7_mighty',
    password='NaamomoDB@21',
    database='proviea7_SunpowerEmployees'

)

my_cursor = myDb.cursor()

my_cursor.execute("show databases")
for db in my_cursor:
    print(db)
