#!python

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import os
from os import scandir, getcwd
from os.path import abspath
import mysql.connector as connector
import numpy as np
from mysql.connector import Error

final_xml_path = "/home/ubuntu/pae/xml/StreamAnalizer/Germany"

def ls(final_xml_path = getcwd()):
        return [arch.name for arch in scandir(final_xml_path) if arch.is_file()]


print ('####### SCRIPT START ##########')
#CONNECTO TO THE DB
#LIST ALL TS
xml_list = ls(final_xml_path)

connection = connector.connect(host='localhost',
                             database='dbTest',
                             user='ubuntu',
                             password='paesa19')
if (connection.is_connected()):
    print ('Connected to the DB')
    cursor = connection.cursor()
else:
    print ('You are currently disconnected')


cursor.execute("SET SQL_SAFE_UPDATES=0;") #later we wont use it but for now its useful to avoid overwriting data
cursor.execute("DELETE FROM PMT;")
cursor.execute("DELETE FROM Video;")

idTS = 0
idPMT = 0
idStream = 0
idVideo = 0
idAudio = 0
idSubtitle = 0

for xml_name in (xml_list):
        fullname = os.path.join(final_xml_path, xml_name)
        print (fullname)
        tree = ET.parse(fullname)
        root = tree.getroot()
        
        
        print ('########################## START TS ########################################')

        #USING ELEMENT TO GET THE PID NUMBER AND DESCRIPTORS
        #TOT SECTION
        for tot in root.findall('{http://www.streamanalyser.com/schema}TOT'):
            recording_time = tot.find('{http://www.streamanalyser.com/schema}UTC_time').text
        country_code = 'GER'
        insertStatement = "INSERT INTO TS (Recording_Date, Country_Code) VALUES ({0}, {1})".format(recording_time, country_code)
        cursor.execute(insertStatement)
        idTS+=1
        #PMT SECTION
        for pmt in root.findall('{http://www.streamanalyser.com/schema}PMT'):
            print ('########### START PMT ##########')
            pid = int(pmt.find('{http://www.streamanalyser.com/schema}PID').text,16)
            print ('PID: ' + str(pid))
            print ('idTS: ' + str(idTS))
            insertStatement = "INSERT INTO PMT (PIDNumber, TS_identifierTS) VALUES ({0}, {1})".format(pid, idTS)
            cursor.execute(insertStatement)
            idPMT +=1

            for streams in pmt.findall('{http://www.streamanalyser.com/schema}Streams'):
                for stream in streams.findall('{http://www.streamanalyser.com/schema}Stream'):
                    print ('###### START STREAM ######')
                    stream_type =  int(stream.find('{http://www.streamanalyser.com/schema}stream_type').text,16)
                    elementary_PID =  int(stream.find('{http://www.streamanalyser.com/schema}elementary_PID').text,16)
                    for streamIdDescriptor in stream.findall('{http://www.streamanalyser.com/schema}StreamIdentifierDescriptor'):
                        component_tag = int(streamIdDescriptor.find('{http://www.streamanalyser.com/schema}component_tag').text,16)
                    print ('STREAM STANDARD: ' + str(component_tag))
                    print ('stream_type: ' + str(stream_type))
                    print ('elementary_PID: ' + str(elementary_PID))
                    
                    #find type of stream and insert the row in corresponent table and row in streams after that relating both
                    if stream_type == 2:
                        print ('VIDEO STREAM')
                        #insert video table row
                        idVideo +=1
                        insertStatement = "INSERT INTO Stream (Elementary_PID, Stream_Type, Stream_Standard, PMT_idPMT, PMT_TS_identifierTS, Video_idVideo) VALUES ({0}, {1}, {2}, {3}, {4}, {5})".format(elementary_PID, stream_type, component_tag, idPMT, idTS, idVideo)
                        cursor.execute(insertStatement)
                        idStream +=1
                    elif stream_type == 3 or stream_type == 4:
                        print ('AUDIO STREAM')
                        for languageDescriptor in stream.findall('{http://www.streamanalyser.com/schema}ISO639LanguageDescriptor'):
                                for language in languageDescriptor.findall('{http://www.streamanalyser.com/schema}Language'):
                                        audio_language = language.find('{http://www.streamanalyser.com/schema}ISO_639_language_code').text
                                        audio_type = int(language.find('{http://www.streamanalyser.com/schema}audio_type').text,16)
                                        print ('AUDIO LANGUAGE: ' + audio_language)
                                        print ('AUDIO TYPE: ' + str(audio_type))
                        insertStatement = "INSERT INTO Audio (Audio_Type, Audio_Language) VALUES ({0}, {1})".format(audio_type, audio_language)
                        cursor.execute(insertStatement)
                        idAudio +=1
                        insertStatement = "INSERT INTO Stream (Elementary_PID, Stream_Type, Stream_Standard, PMT_idPMT, PMT_TS_identifierTS, Audio_idAudio) VALUES ({0}, {1}, {2}, {3}, {4}, {5})".format(elementary_PID, stream_type, component_tag, idPMT, idTS, idAudio)
                        cursor.execute(insertStatement)
                        idStream +=1

                    elif stream_type == 6:
                        for child in stream:
                                if child.tag == '{http://www.streamanalyser.com/schema}SubtitlingDescriptor':
                                        print ('SUBTITLES STREAM')
                                        for subDescriptor in stream.findall('{http://www.streamanalyser.com/schema}SubtitlingDescriptor'):
                                                for subtitle in subDescriptor.findall('{http://www.streamanalyser.com/schema}Subtitle'):
                                                        subtitle_language = subtitle.find('{http://www.streamanalyser.com/schema}ISO_639_language_code').text
                                                        subtitle_type = int(subtitle.find('{http://www.streamanalyser.com/schema}subtitling_type').text,16)
                                                        print ('SUBTITLE LANGUAGE: ' + subtitle_language)
                                                        print ('SUBTITLE TYPE: ' + str(subtitle_type))
                        insertStatement = "INSERT INTO Subtitles (Subtitles_Language) VALUES ({0})".format(subtitle_language)
                        cursor.execute(insertStatement)
                        idSubtitle +=1
                        insertStatement = "INSERT INTO Stream (Elementary_PID, Stream_Type, Stream_Standard, PMT_idPMT, PMT_TS_identifierTS, Subtitles_idSubtitles) VALUES ({0}, {1}, {2}, {3}, {4}, {5})".format(elementary_PID, stream_type, component_tag, idPMT, idTS, idSubtitle)
                        cursor.execute(insertStatement)
                        idStream +=1

                    print ('##### END STREAM #####')
            print ('########### END PMT ##########')
            #VIDEO SECTION
            for video in root.findall('{http://www.streamanalyser.com/schema}Video'):
                print ('########## START VIDEO ###########')
                elementary_PID = int(video.find('{http://www.streamanalyser.com/schema}PID').text,16)
                video_type = int(video.find('{http://www.streamanalyser.com/schema}Type').text,16)
                for info in video.findall('{http://www.streamanalyser.com/schema}Info'):
                    width = int(info.find('{http://www.streamanalyser.com/schema}Width').text)
                    height = int(info.find('{http://www.streamanalyser.com/schema}Height').text)
                print ('VIDEO PID: ' + str(elementary_PID))
                print ('VIDEO TYPE: ' + str(video_type))
                print ('RESOLUTION: ' + str(width) + ', ' + str(height))
                print ('########## END VIDEO ############')
        print ('########################## END TS ####################################')

connection.commit()
cursor.close()
connection.close()
print ('####### SCRIPT END ##########')
