#!python

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import os
from os import scandir, getcwd
from os.path import abspath
import mysql.connector as connector
import numpy as np
from mysql.connector import Error

final_xml_path = "/home/ubuntu/pae/xml/MergerTeam"

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

        for tot in root.findall('{http://www.streamanalyser.com/schema}Information'):
            country_code = tot.find('{http://www.streamanalyser.com/schema}Country').text
            comment = tot.find('{http://www.streamanalyser.com/schema}Comment').text
            frequency = tot.find('{http://www.streamanalyser.com/schema}Frequency').text
            path = tot.find('{http://www.streamanalyser.com/schema}Path').text
            tipe = tot.find('{http://www.streamanalyser.com/schema}Type').text
            if tipe == 'Satellite':
                orbital_position = tot.find('{http://www.streamanalyser.com/schema}Orbital_Position').text
            elif tipe == 'Cable':
                operator = tot.find('{http://www.streamanalyser.com/schema}Operator').text

        #TOT SECTION
        for tot in root.findall('{http://www.streamanalyser.com/schema}TOT'):
            recording_time = tot.find('{http://www.streamanalyser.com/schema}UTC_time').text

        idTS +=1
        insertStatement = "INSERT INTO TS (identifierTS, Recording_Date, Country_Code, Tipo, Comment, Frequency, Operator, Orbital_Position, Path) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(xml_name, recording_time, country_code, tipe, comment, frequency, operator, orbital_position, path)
        cursor.execute(insertStatement)

        #PMT SECTION
        for pmt in root.findall('{http://www.streamanalyser.com/schema}PMT'):
            pid = int(pmt.find('{http://www.streamanalyser.com/schema}PID').text,16)
            idPMT +=1
            insertStatement = "INSERT INTO PMT (idPMT, PIDNumber, identifierTS) VALUES ({0}, {1}, '{2}')".format(idPMT, pid, xml_name)
            cursor.execute(insertStatement)

            for streams in pmt.findall('{http://www.streamanalyser.com/schema}Streams'):
                for stream in streams.findall('{http://www.streamanalyser.com/schema}Stream'):
                    stream_type =  int(stream.find('{http://www.streamanalyser.com/schema}stream_type').text,16)
                    elementary_PID =  int(stream.find('{http://www.streamanalyser.com/schema}elementary_PID').text,16)
                    for streamIdDescriptor in stream.findall('{http://www.streamanalyser.com/schema}StreamIdentifierDescriptor'):
                        component_tag = int(streamIdDescriptor.find('{http://www.streamanalyser.com/schema}component_tag').text,16)
                    #find type of stream and insert the row in corresponent table and row in streams after that relating both
                    if stream_type == 2 or stream_type == 36:
                        #insert video table row
                        idVideo +=1
                        #####insert######
                        W=50
                        H=50
                        I=1
                        name = 'test'
                        insertStatement = "INSERT INTO Video (idVideo, Width, Height, Interlaced, TypeName) VALUES ({0}, {1}, {2}, {3}, '{4}')".format(idVideo, W, H, I, name)
                        cursor.execute(insertStatement)
                        idStream +=1
                        insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', {6}, NULL, NULL, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idVideo)
                        cursor.execute(insertStatement)
                    elif stream_type == 3 or stream_type == 4:
                        for languageDescriptor in stream.findall('{http://www.streamanalyser.com/schema}ISO639LanguageDescriptor'):
                                for language in languageDescriptor.findall('{http://www.streamanalyser.com/schema}Language'):
                                        audio_language = language.find('{http://www.streamanalyser.com/schema}ISO_639_language_code').text
                                        audio_type = int(language.find('{http://www.streamanalyser.com/schema}audio_type').text,16)
                        idAudio +=1
                        insertStatement = "INSERT INTO Audio (idAudio, Audio_Type, Audio_Language) VALUES ({0}, {1}, '{2}')".format(idAudio, audio_type, audio_language)
                        cursor.execute(insertStatement)
                        idStream +=1
                        insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, {6}, NULL, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idAudio)
                        cursor.execute(insertStatement)

                    elif stream_type == 6:
                        for child in stream:
                                if child.tag == '{http://www.streamanalyser.com/schema}SubtitlingDescriptor':
                                        for subDescriptor in stream.findall('{http://www.streamanalyser.com/schema}SubtitlingDescriptor'):
                                                for subtitle in subDescriptor.findall('{http://www.streamanalyser.com/schema}Subtitle'):
                                                        subtitle_language = subtitle.find('{http://www.streamanalyser.com/schema}ISO_639_language_code').text
                                                        subtitle_type = int(subtitle.find('{http://www.streamanalyser.com/schema}subtitling_type').text,16)
                                                        idSubtitle +=1
                                                        insertStatement = "INSERT INTO Subtitles (idSubtitles, Subtitles_Language) VALUES ({0}, '{1}')".format(idSubtitle, subtitle_language)
                                                        cursor.execute(insertStatement)
                                                        idStream +=1
                                                        insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, NULL, {6}, NULL)".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idSubtitle)
                                                        cursor.execute(insertStatement)

                                if child.tag == '{http://www.streamanalyser.com/schema}TeletextDescriptor':
                                        for teletextDescriptor in stream.findall('{http://www.streamanalyser.com/schema}TeletextDescriptor'):
                                                for teletext in teletextDescriptor.findall('{http://www.streamanalyser.com/schema}Teletext'):
                                                        teletext_language = teletext.find('{http://www.streamanalyser.com/schema}ISO_639_language_code').text
                                                        idTeletext +=1
                                                        insertStatement = "INSERT INTO Teletext (idTeletext, Teletext_Language) VALUES ({0}, '{1}')".format(idTeletext, teletext_language)
                                                        cursor.execute(insertStatement)
                                                        idStream +=1
                                                        insertStatement = "INSERT INTO Stream (idStream, Elementary_PID, Stream_Type, Stream_Standard, idPMT, identifierTS, idVideo, idAudio, idSubtitles, idTeletext) VALUES ({0}, {1}, {2}, {3}, {4}, '{5}', NULL, NULL, NULL, {6})".format(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idTeletext)
                                                        cursor.execute(insertStatement)


            #VIDEO SECTION
            for video in root.findall('{http://www.streamanalyser.com/schema}Video'):
                elementary_PID = int(video.find('{http://www.streamanalyser.com/schema}PID').text,16)
                video_type = int(video.find('{http://www.streamanalyser.com/schema}Type').text,16)
                for info in video.findall('{http://www.streamanalyser.com/schema}Info'):
                    width = int(info.find('{http://www.streamanalyser.com/schema}Width').text)
                    height = int(info.find('{http://www.streamanalyser.com/schema}Height').text)
        print ('########################## END TS ####################################')

connection.commit()


cursor.close()
connection.close()
print ('####### SCRIPT END ##########')
