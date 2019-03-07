# -*- coding: utf-8 -*-
#!python

import xml.etree.ElementTree as ET
import mysql.connector as connector
import numpy as np
from mysql.connector import Error

try:
        connection = connector.connect(host='localhost',
                             database='mydb',
                             user='root',
                             password='Nacia321')
    
        if connection.is_connected():
            print ('Connectat')
            cursor = connection.cursor()
        else:
            print ('You are currently disconnected')
except Error as e:
    print ('Error. ')
       

   


print ('####### SCRIPT START ##########')
tree = ET.parse('C_KBW_DE_Stuttgart_20130114_394MHz_256QAM_6900sym_SkyAktion_Guide-TSReader.xml')
#we need to contemplate the way to get the names of the xml files for the ET.parse
root = tree.getroot()

#EXAMPLE OF USING TREE HIERARCHY TO GET THE CHILD WE WANT
data =[]

#USING ELEMENT TO GET THE PID NUMBER AND DESCRIPTORS
for pid_usage in root.findall('PID-USAGE'):
    for pid in pid_usage.findall('PID'):
        #I already cast the text of number to an hexadecimal number var
        number =  (int(pid.find('NUMBER').text,16))
        description = pid.find('DESCRIPTION').text
        data.append(number, description)
        
        
      
        #here we need to call the function that inputs data to the database for each number and description
    #sqlcomm = """INSERT INTO 'PID' ('PID_number', 'Description') VALUES (%d, %s)"""
sqlcomm= """INSERT INTO PID (PID_number, Description) VALUES (%s, %s);"""
print(data)
cursor.executemany(sqlcomm, data)
    #cursor.executemany(sqlcomm, data)
connection.commit() 
print ('Fetching a table...')
    
name_of_table = ('PID')


sql_select_Query = ("SELECT * FROM PID")

cursor.execute(sql_select_Query)
table = cursor.fetchall()
for row in table:
    print (row)
    
##########################################################################
#SubScript checks if a value is duplicated

#returns -1 if the PID does not exists
def checkDuplicated(cursor,PID_under_test):
  pre_sql_query = "SELECT IFNULL(table1.PID,-1) FROM table1 WHERE PID="
  sql_query = pre_sql_query + str(PID_under_test)
  cursor.excute(sql_query)
  return cursor.fetchone()

if(checkDuplicated(cursor,PID_under_test)==-1):
  #can insert value safely
 
##########################################################################
cursor.close()
connection.close()
print ('####### SCRIPT END ##########')
      
