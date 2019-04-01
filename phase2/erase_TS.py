#!/bin/python

import sys
import mysql.connector as connector
import numpy as np
from mysql.connector import Error
from queries_mysql import *


def erase_old_TS (xml_list, cursor):
    
    TS_list = obtain_TS (cursor)
    for name in TS_list:
        if name not in xml_list:
            print ("Deleting " + name + " from the Database")
            PMT_list = obtain_PMTs_fromTS (name, cursor)
            Stream_list = obtain_Streams_fromTS (name, cursor)
            Video_list = obtain_Videos_fromTS (name, cursor)
            Audio_list = obtain_Audios_fromTS (name, cursor)
            Subtitles_list = obtain_Subtitles_fromTS (name, cursor)
            Teletext_list = obtain_Teletext_fromTS (name, cursor)
            Private_list = obtain_Private_fromTS (name, cursor)
            print (PMT_list)
            print (Stream_list)
            print (Video_list)
            print (Audio_list)
            print (Subtitles_list)
            print (Teletext_list)
            for Video in Video_list:
                delete_Video (Video, cursor)
            for Audio in Audio_list:
                delete_Audio (Audio, cursor)
            for Subtitle in Subtitles_list:
                delete_Subtitle (Subtitle, cursor)
            for Teletext in Teletext_list:
                delete_Teletext (Teletext, cursor)
            for Private in Private_list:
                URL_list = obtain_URL_fromTS (Private, cursor)
                print (URL_list)
                for URL in URL_list:
                    delete_URL (URL, cursor)
                delete_Private (Private, cursor)
            for Stream in Stream_list:
                delete_Stream (Stream, cursor)
            for PMT in PMT_list:
                delete_PMT (PMT, cursor)
            delete_TS (name, cursor)
            print ("All data from " + name +" DELETED")

