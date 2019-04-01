#!python

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import mysql.connector as connector
import numpy as np
from mysql.connector import Error
from queries_mysql import *
import constants as cte

def obtainData (fullname, xml_name, cursor, idPMT, idStream, idVideo, idAudio, idSubtitle, idTeletext, idPrivate, idURL):
    tag ="{http://www.streamanalyser.com/schema}"
    tree = ET.parse(fullname)
    root = tree.getroot()
            
    #TS SECTION
    #INFO SECTION
    orbital_position = 'NULL'
    operator = 'NULL'
    for inf in root.findall(tag+'Information'):
        country_code = inf.find(tag+'Country').text
        comment = inf.find(tag+'Comment').text
        frequency = inf.find(tag+'Frequency').text
        path = inf.find(tag+'Path').text
        tipe = inf.find(tag+'Type').text
        if tipe == 'Satellite':
            orbital_position = inf.find(tag+'Orbital_Position').text
        elif tipe == 'Cable':
            operator = inf.find(tag+'Operator').text

    #TOT SECTION
    recording_time = "not defined"
    for tot in root.findall(tag+'TOT'):
        recording_time = tot.find(tag+'UTC_time').text
    insert_TS(xml_name, recording_time, country_code, tipe, comment, frequency, operator, orbital_position, path, cursor)

    #PMT SECTION
    for pmt in root.findall(tag+'PMT'):
        pid = int(pmt.find(tag+'PID').text,16)
        #TO DO NEW PARAMETERS OF PMT
        num_onid = 0
        name_onid = "TO DO"
        network_onid = "TO DO"
        country_onid = "TO DO"
        idPMT +=1
        insert_PMT(idPMT, pid, xml_name, num_onid, name_onid, network_onid, country_onid, cursor)
        #STREAM SECTION
        for streams in pmt.findall(tag+'Streams'):
            for stream in streams.findall(tag+'Stream'):
                stream_type =  int(stream.find(tag+'stream_type').text,16)
                elementary_PID =  int(stream.find(tag+'elementary_PID').text,16)
                component_tag = cte.MISSING
                for streamIdDescriptor in stream.findall(tag+'StreamIdentifierDescriptor'):
                    component_tag = int(streamIdDescriptor.find(tag+'component_tag').text,16)
                #TYPE SECTION
                #find type of stream and insert the row in corresponent table and row in streams after that relating both
                if stream_type == cte.VIDEO_MPEG or stream_type == cte.VIDEO_HEVC or stream_type == cte.VIDEO_AVC:
                    #VIDEO SECTION
                    width=0
                    height=0
                    interlaced=(cte.MISSING)
                    video_typename = 'not defined'
                    for child in root:
                        if child.tag == (tag+'Video'):
                            for video in root.findall(tag+'Video'):
                                video_PID = int(video.find(tag+'PID').text,16)
                                if video_PID == elementary_PID:
                                    video_service = int(video.find(tag+'Service').text,16)
                                    video_typename = video.find(tag+'TypeName').text
                                    video_type = int(video.find(tag+'Type').text,16)
                                    for info in video.findall(tag+'Info'):
                                        width = int(info.find(tag+'Width').text)
                                        height = int(info.find(tag+'Height').text)
                                        interlaced=int(info.find(tag+'Interlaced').text)
                    #OBTINING NEW PARAMETERS OF VIDEO 
                    bit_rate_mode = "TO DO"
                    pixel_aspect_ratio = 0
                    display_aspect_ratio = 0
                    frame_rate = 0
                    idVideo +=1
                    insert_Video(idVideo, width, height, interlaced, video_typename, bit_rate_mode, pixel_aspect_ratio, display_aspect_ratio, frame_rate, cursor)
                    idStream +=1
                    insert_Stream_Video(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idVideo, cursor)
                elif stream_type == cte.AUDIO_MPEG_1 or stream_type == cte.AUDIO_MPEG_2 or stream_type == cte.AUDIO_MPEG4_AAC or stream_type == cte.AUDIO_MPEG_AAC or stream_type == cte.AUDIO_AC3 or stream_type == cte.AUDIO_DTS:
                    #AUDIO SECTION
                    audio_type = cte.MISSING
                    audio_language = 'not defined'
                    for languageDescriptor in stream.findall(tag+'ISO639LanguageDescriptor'):
                            for language in languageDescriptor.findall(tag+'Language'):
                                    audio_language = language.find(tag+'ISO_639_language_code').text
                                    audio_type = int(language.find(tag+'audio_type').text,16)
                    #OBTAINING NEW PARAMETERS OF AUDIO
                    bit_rate_mode = "TO DO"
                    bit_rate = 0
                    channels = "TO DO"
                    frame_rate = 0
                    idAudio +=1
                    insert_Audio(idAudio, audio_type, audio_language, bit_rate_mode, bit_rate, channels, frame_rate, cursor)
                    idStream +=1
                    insert_Stream_Audio(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idAudio, cursor)
                elif stream_type == cte.TEXT:
                    #DATA SECTION
                    for child in stream:
                            #SUBTITLES SECTION
                            if child.tag == (tag+'SubtitlingDescriptor'):
                                    for subDescriptor in stream.findall(tag+'SubtitlingDescriptor'):
                                            for subtitle in subDescriptor.findall(tag+'Subtitle'):
                                                    subtitle_language = subtitle.find(tag+'ISO_639_language_code').text
                                                    idSubtitle +=1
                                                    insert_Subtitles(idSubtitle, subtitle_language, cursor)
                                                    idStream +=1
                                                    insert_Stream_Subtitles(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idSubtitle, cursor)
                            #TELETEXT SECTION
                            if child.tag == (tag+'TeletextDescriptor'):
                                    for teletextDescriptor in stream.findall(tag+'TeletextDescriptor'):
                                            for teletext in teletextDescriptor.findall(tag+'Teletext'):
                                                    teletext_language = teletext.find(tag+'ISO_639_language_code').text
                                                    idTeletext +=1
                                                    insert_Teletext(idTeletext, teletext_language, cursor)
                                                    idStream +=1
                                                    insert_Stream_Teletext(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idTeletext, cursor)
                elif stream_type == cte.PRIVATE:
                    #PRIVATE SECTION
                    for child in stream:
                        #OBTAINING DATA FROM PRIVATE
                        private_standard = "TO DO"
                        idPrivate +=1
                        insert_Private(idPrivate, private_standard, cursor)
                        #OBTAIN ALL THE URL ASSIGNED TO THIS PRIVATE
                        url = "TO DO"
                        idURL +=1
                        insert_URL(idURL, url, idPrivate, cursor)
                        #at the end we insert the corresponding stream
                        idStream +=1
                        insert_Stream_Private(idStream, elementary_PID, stream_type, component_tag, idPMT, xml_name, idPrivate, cursor)
