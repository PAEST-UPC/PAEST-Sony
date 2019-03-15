#!python

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import os
from os import scandir, getcwd
from os.path import abspath

print ('####### SCRIPT START ##########')
#connect to the db

final_xml_path = "/home/ubuntu/pae/xml/StreamAnalizer/Germany"

def ls(final_xml_path = getcwd()):
        #absolute xml path
        #return [abspath(arch.path) for arch in scandir(final_xml_path) if arch.is_file()]
        #only xml filename
        return [arch.name for arch in scandir(final_xml_path) if arch.is_file()]

xml_list = ls(final_xml_path)

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
        #PMT SECTION
        for pmt in root.findall('{http://www.streamanalyser.com/schema}PMT'):
            print ('########### START PMT ##########')
            pid = hex(int(pmt.find('{http://www.streamanalyser.com/schema}PID').text,16))
            idTable = hex(int(pmt.find('{http://www.streamanalyser.com/schema}table_id').text,16))
            print ('PID: ' + pid)
            print ('table id: ' + idTable)

            for streams in pmt.findall('{http://www.streamanalyser.com/schema}Streams'):
                for stream in streams.findall('{http://www.streamanalyser.com/schema}Stream'):
                    print ('###### START STREAM ######')
                    stream_type =  hex(int(stream.find('{http://www.streamanalyser.com/schema}stream_type').text,16))
                    elementary_PID =  hex(int(stream.find('{http://www.streamanalyser.com/schema}elementary_PID').text,16))
                    print ('stream_type: ' + stream_type)
                    print ('elementary_PID: ' + elementary_PID)
                    if stream_type == hex(2) or stream_type == hex(36):
                        print ('VIDEO STREAM')
                        for streamIdDescriptor in stream.findall('{http://www.streamanalyser.com/schema}StreamIdentifierDescriptor'):
                                component_tag = hex(int(streamIdDescriptor.find('{http://www.streamanalyser.com/schema}component_tag').text,16))
                                print ('COMPONENT TAG: ' + component_tag)
                    elif stream_type == hex(3) or stream_type == hex(4):
                        print ('AUDIO STREAM')
                        for streamIdDescriptor in stream.findall('{http://www.streamanalyser.com/schema}StreamIdentifierDescriptor'):
                                component_tag = hex(int(streamIdDescriptor.find('{http://www.streamanalyser.com/schema}component_tag').text,16))
                                print ('COMPONENT TAG: ' + component_tag)
                        for languageDescriptor in stream.findall('{http://www.streamanalyser.com/schema}ISO639LanguageDescriptor'):
                                for language in languageDescriptor.findall('{http://www.streamanalyser.com/schema}Language'):
                                        audio_language = language.find('{http://www.streamanalyser.com/schema}ISO_639_language_code').text
                                        audio_type = hex(int(language.find('{http://www.streamanalyser.com/schema}audio_type').text,16))
                                        print ('AUDIO LANGUAGE: ' + audio_language)
                                        print ('AUDIO TYPE: ' + audio_type)
                    elif stream_type == hex(6):
                        for streamIdDescriptor in stream.findall('{http://www.streamanalyser.com/schema}StreamIdentifierDescriptor'):
                                component_tag = hex(int(streamIdDescriptor.find('{http://www.streamanalyser.com/schema}component_tag').text,16))
                                print ('STREAM STANDARD: ' + component_tag)
                        for child in stream:
                                if child.tag == '{http://www.streamanalyser.com/schema}SubtitlingDescriptor':
                                        print ('SUBTITLES STREAM')
                                        for subDescriptor in stream.findall('{http://www.streamanalyser.com/schema}SubtitlingDescriptor'):
                                                for subtitle in subDescriptor.findall('{http://www.streamanalyser.com/schema}Subtitle'):
                                                        subtitle_language = subtitle.find('{http://www.streamanalyser.com/schema}ISO_639_language_code').text
                                                        subtitle_type = hex(int(subtitle.find('{http://www.streamanalyser.com/schema}subtitling_type').text,16))
                                                        print ('SUBTITLE LANGUAGE: ' + subtitle_language)
                                                        print ('SUBTITLE TYPE: ' + subtitle_type)
                    print ('##### END STREAM #####')
            #VIDEO SECTION
            print ('########### END PMT ##########')
            for video in root.findall('{http://www.streamanalyser.com/schema}Video'):
                print ('########## START VIDEO ###########')
                elementary_PID = hex(int(video.find('{http://www.streamanalyser.com/schema}PID').text,16))
                video_type = hex(int(video.find('{http://www.streamanalyser.com/schema}Type').text,16))
                for info in video.findall('{http://www.streamanalyser.com/schema}Info'):
                    width = int(info.find('{http://www.streamanalyser.com/schema}Width').text)
                    height = int(info.find('{http://www.streamanalyser.com/schema}Height').text)
                print ('VIDEO PID: ' + elementary_PID)
                print ('VIDEO TYPE: ' + video_type)
                print ('RESOLUTION: ' + str(width) + ', ' + str(height))
                print ('########## END VIDEO ############')
        print ('########################## END TS ####################################')
print ('####### SCRIPT END ##########')
