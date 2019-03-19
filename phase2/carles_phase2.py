#!python

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import os
from os import scandir, getcwd
from os.path import abspath
import mysql.connector as connector
import numpy as np
from mysql.connector import Error
from inserts_mysql import *

final_xml_path = "/home/ubuntu/pae/xml/MergerTeam"
tag ="{http://www.streamanalyser.com/schema}"

def ls(final_xml_path = getcwd()):
        return [arch.name for arch in scandir(final_xml_path) if arch.is_file()]


print ('####### SCRIPT START ##########')
#CONNECTO TO THE DB
#LIST ALL TS
xml_list = ls(final_xml_path)

connection = connector.connect(host='localhost',
                             database='dbPhase2',
                             user='ubuntu',
                             password='paesa19')
if (connection.is_connected()):
    print ('Connected to the DB')
    cursor = connection.cursor()
else:
    print ('You are currently disconnected')


idTS = 0
idPMT = 0
idStream = 0
idVideo = 0
idAudio = 0
idSubtitle = 0
idTeletext = 0

for xml_name in (xml_list):
        fullname = os.path.join(final_xml_path, xml_name)
        print (fullname)
        tree = ET.parse(fullname)
        root = tree.getroot()
        
        
        print ('########################## START TS ########################################')

        #USING ELEMENT TO GET THE PID NUMBER AND DESCRIPTORS
        #INFO SECTION
        orbital_position = 'NULL'
        operator = 'NULL'
        for tot in root.findall(tag+'Information'):
            country_code = tot.find(tag+'Country').text
            comment = tot.find(tag+'Comment').text
            frequency = tot.find(tag+'Frequency').text
            path = tot.find(tag+'Path').text
            tipe = tot.find(tag+'Type').text
            if tipe == 'Satellite':
                orbital_position = tot.find(tag+'Orbital_Position').text
            elif tipe == 'Cable':
                operator = tot.find(tag+'Operator').text

        #TOT SECTION
        for tot in root.findall(tag+'TOT'):
            recording_time = tot.find(tag+'UTC_time').text

        idTS +=1
        insert_TS(xml_name, recording_time, country_code, tipe, comment, frequency, operator, orbital_position, path, cursor)

        #PMT SECTION
        for pmt in root.findall(tag+'PMT'):
            pid = int(pmt.find(tag+'PID').text,16)
            idPMT +=1
            insert_PMT(idPMT, pid, xml_name, cursor)

            for streams in pmt.findall(tag+'Streams'):
                for stream in streams.findall(tag+'Stream'):
                    stream_type =  int(stream.find(tag+'stream_type').text,16)
                    elementary_PID =  int(stream.find(tag+'elementary_PID').text,16)
                    for streamIdDescriptor in stream.findall(tag+'StreamIdentifierDescriptor'):
                        component_tag = int(streamIdDescriptor.find(tag+'component_tag').text,16)
                    #find type of stream and insert the row in corresponent table and row in streams after that relating both
                    if stream_type == 2 or stream_type == 36:
                        #insert video table row
                        idVideo +=1
                        #####insert######
                        W=50
                        H=50
                        I=1
                        name = 'test'
                        insert_Video(idVideo, W, H, I, name, cursor)                        
                        idStream +=1
                        insert_Stream_Video(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idVideo, cursor)
                    elif stream_type == 3 or stream_type == 4:
                        for languageDescriptor in stream.findall(tag+'ISO639LanguageDescriptor'):
                                for language in languageDescriptor.findall(tag+'Language'):
                                        audio_language = language.find(tag+'ISO_639_language_code').text
                                        audio_type = int(language.find(tag+'audio_type').text,16)
                        idAudio +=1
                        insert_Audio(idAudio, audio_type, audio_language, cursor)
                        idStream +=1
                        insert_Stream_Audio(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idAudio, cursor)

                    elif stream_type == 6:
                        for child in stream:
                                if child.tag == (tag+'SubtitlingDescriptor'):
                                        for subDescriptor in stream.findall(tag+'SubtitlingDescriptor'):
                                                for subtitle in subDescriptor.findall(tag+'Subtitle'):
                                                        subtitle_language = subtitle.find(tag+'ISO_639_language_code').text
                                                        idSubtitle +=1
                                                        insert_Subtitles(idSubtitle, subtitle_language, cursor)
                                                        idStream +=1
                                                        insert_Stream_Subtitles(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idSubtitle, cursor)

                                if child.tag == (tag+'TeletextDescriptor'):
                                        for teletextDescriptor in stream.findall(tag+'TeletextDescriptor'):
                                                for teletext in teletextDescriptor.findall(tag+'Teletext'):
                                                        teletext_language = teletext.find(tag+'ISO_639_language_code').text
                                                        idTeletext +=1
                                                        insert_Teletext(idTeletext, teletext_language, cursor)
                                                        idStream +=1
                                                        insert_Stream_Teletext(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idTeletext, cursor)


            #VIDEO SECTION
            for video in root.findall(tag+'Video'):
                elementary_PID = int(video.find(tag+'PID').text,16)
                video_type = int(video.find(tag+'Type').text,16)
                for info in video.findall(tag+'Info'):
                    width = int(info.find(tag+'Width').text)
                    height = int(info.find(tag+'Height').text)
        print ('########################## END TS ####################################')

connection.commit()


cursor.close()
connection.close()
print ('####### SCRIPT END ##########')
