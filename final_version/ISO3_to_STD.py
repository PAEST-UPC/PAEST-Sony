#! /usr/bin/python
import xml.etree.ElementTree as ET
import os
import xlrd
from xlrd import open_workbook
import mysql.connector as connector
from mysql.connector import Error



connection = connector.connect(host='localhost',
                                 database='dictionary',
                                 user='ubuntu',
                                 password='paesa19')
if (connection.is_connected()):
    print ('Connected to the DB')
    cursor = connection.cursor()
else:
    print ('You are currently disconnected')

wbk = xlrd.open_workbook("/home/ubuntu/pae/scripts/DBTeam/TranslationTable_ISO3toSTD.xls")
sheet_names = wbk.sheet_names()
sheet = wbk.sheet_by_index(0)
for row in range(0, sheet.nrows):
    cell_obj = sheet.cell(row, 0)
    iso = cell_obj.value
    cell_obj = sheet.cell(row, 2)
    meaning = cell_obj.value
    insertStatement = "INSERT INTO Dictionary (var_obtained, Value, Type, Meaning) VALUES ('Audio_Language', '{0}', 'Audio', '{1}')".format(iso, meaning)
    cursor.execute(insertStatement)
    insertStatement = "INSERT INTO Dictionary (var_obtained, Value, Type, Meaning) VALUES ('Teletext_Language', '{0}', 'Teletext', '{1}')".format(iso, meaning)
    cursor.execute(insertStatement)
    insertStatement = "INSERT INTO Dictionary (var_obtained, Value, Type, Meaning) VALUES ('Subtitles_Language', '{0}', 'Subtitles', '{1}')".format(iso, meaning)
    cursor.execute(insertStatement)

connection.commit()
cursor.close()
connection.close()

