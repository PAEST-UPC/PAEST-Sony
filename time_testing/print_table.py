#!/bin/python
import sys
import mysql.connector as connector
from mysql.connector import Error

if (len(sys.argv)==3):
    connection = connector.connect(host='localhost',
                                 database=sys.argv[1],
                                 user='ubuntu',
                                 password='paesa19')
    if (connection.is_connected()):
        print ('Connected to ' + str(sys.argv[1]))
        cursor = connection.cursor()
        sql_select_Query = ("SELECT * FROM " + str(sys.argv[2]))
        cursor.execute(sql_select_Query)
        table = cursor.fetchall()
        for row in table:
            print (row)
    else:
        print ('You are currently disconnected')
        print ('Database incorrect')
    cursor.close()
    connection.close()
else:
    print ('ERROR')
    print ('Please use the correct format: python3 delete_all_data.py dbname tableName')

