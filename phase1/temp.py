# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!python

import xml.etree.ElementTree as ET
import mysql.connector as connector
import numpy as np
from mysql.connector import Error
import os
from os import scandir, getcwd
from os.path import abspath


#final_xml_path = "/Users/nataliaszakiel/Desktop/PAE/XMLS2"
#
#def ls(final_xml_path = getcwd()):
#        #absolute xml path
#        #return [abspath(arch.path) for arch in scandir(final_xml_path) if arch.is_file()]
#        #only xml filename
#        return [arch.name for arch in scandir(final_xml_path) if arch.is_file()]
#xml_list = ls(final_xml_path)



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



#for i in range (0,len(xml_list)):
#       
#        fullname = os.path.join(final_xml_path, xml_list[i])
#        print (i)
#        print ("####")
#        print (fullname)
#
#        tree = ET.parse(fullname)
#        root = tree.getroot()


#EXAMPLE OF USING TREE HIERARCHY TO GET THE CHILD WE WANT
i=0
parameters = [ ]
cursor.execute("SET SQL_SAFE_UPDATES=0;") #later we wont use it but for now its useful to avoid overwriting data
cursor.execute("DELETE FROM PMT;")

#USING ELEMENT TO GET THE PID NUMBER AND DESCRIPTORS
for pid_usage in root.findall('PID-USAGE'):
    for pid in pid_usage.findall('PID'):
        #I already cast the text of number to an hexadecimal number var
        number =  (int(pid.find('NUMBER').text,16))
        description = pid.find('DESCRIPTION').text
        parameters.append([])
        parameters[i].append(number)
        parameters[i].append(description)
        i +=1
    
    
        #here we need to call the function that inputs data to the database for each number and description
        #sqlcomm = """INSERT INTO 'PID' ('PID_number', 'Description') VALUES (%d, %s)"""
#print(parameters)
sql_comm= """INSERT INTO PID (PID_number, Description) VALUES (%s, %s);"""
result  = cursor.executemany(sql_comm, parameters)
connection.commit() 


sql_select_Query = ("SELECT * FROM PID")

cursor.execute(sql_select_Query)
table = cursor.fetchall()
for row in table:
    print (row)
cursor.close()
connection.close()
print ('####### SCRIPT END ##########')
      
