#!/bin/python
import sys
import mysql.connector as connector
import numpy as np
from mysql.connector import Error

if (len(sys.argv)==2):
    connection = connector.connect(host='localhost',
                                 database=sys.argv[1],
                                 user='ubuntu',
                                 password='paesa19')
    if (connection.is_connected()):
        print ('Connected to ' + str(sys.argv[1]))
        print ('Erasing all data...')
        cursor = connection.cursor()
        cursor.execute("SET SQL_SAFE_UPDATES=0;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE Video;")
        cursor.execute("TRUNCATE TABLE Audio;")
        cursor.execute("TRUNCATE TABLE Subtitles;")
        cursor.execute("TRUNCATE TABLE Teletext;")
        cursor.execute("TRUNCATE TABLE TS;")
        cursor.execute("TRUNCATE TABLE PMT;")
        cursor.execute("TRUNCATE TABLE Stream;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print ('Data erased!')

    else:
        print ('You are currently disconnected')
        print ('Database incorrect')
    cursor.close()
    connection.close()
else:
    print ('ERROR')
    print ('Please use the correct format: python3 delete_all_data.py dbname')

