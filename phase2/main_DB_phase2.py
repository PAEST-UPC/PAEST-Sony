#!python

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import os
import sys
from os import scandir, getcwd
from os.path import abspath
import mysql.connector as connector
import numpy as np
from mysql.connector import Error
from queries_mysql import *
from obtain_data import *

final_xml_path = "/home/ubuntu/pae/xml/MergerTeam"

def ls(final_xml_path = getcwd()):
        return [arch.name for arch in scandir(final_xml_path) if arch.is_file()]

if (len(sys.argv)==2):
    print ('####### SCRIPT START ##########')

    connection = connector.connect(host='localhost',
                                 database=sys.argv[1],
                                 user='ubuntu',
                                 password='paesa19')
    if (connection.is_connected()):
        print ('Connected to the DB')
        cursor = connection.cursor()
    else:
        print ('You are currently disconnected')
    
    TS_list = []
    TS_mysql_list = obtain_TS(cursor)
    for name in TS_mysql_list:
        name = str(name)
        x = name.split("'")
        TS_list.append(x[1])

    xml_list = ls(final_xml_path)
    for xml_name in (xml_list):
        print (xml_name)
        if xml_name in TS_list:
            print ("xml_already in DB")
        else:
            print ("Obtaining Data...")
            idPMT = obtain_PMT(cursor)
            idStream = obtain_Stream(cursor)
            idVideo = obtain_Video(cursor)
            idAudio = obtain_Audio(cursor)
            idSubtitle = obtain_Subtitles(cursor)
            idTeletext = obtain_Teletext(cursor)
            fullname = os.path.join(final_xml_path, xml_name)
            obtainData(fullname, xml_name, cursor, idPMT, idStream, idVideo, idAudio, idSubtitle, idTeletext)
            print ("Data obtained!")

            
    connection.commit()
    cursor.close()
    connection.close()
    print ('####### SCRIPT END ##########')
else:
    print ('ERROR')
    print ('Please use the correct format: python3 delete_all_data.py dbname')

