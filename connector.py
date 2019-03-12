#module mysql-connector-python is required to perform the connection
#it can be installed pip install mysql-connector-python#

import mysql.connector as connector
from mysql.connector import Error

def connect_to_db():
    try:
        connection = connector.connect(host='localhost',
                             database='dbTest',
                             user='ubuntu',
                             password='paesa19')
    
        if (connection.is_connected()):
            print ('Connectat')
            cursor = connection.cursor()
        else:
            print ('You are currently disconnected')
    except Error as e:
        print ('Error. ')
        return 0
    print ('Fetching a table...')
    sql_select_Query = ("SELECT * FROM" + "PMT")
#    cursor.execute(sql_select_Query)
#    table = cursor.fetchall()
#    for row in table:
#        print (row)
#    cursor.close()
    connection.close()
    return
    
connect_to_db()
