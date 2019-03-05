#!python

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import os
from os import scandir, getcwd
from os.path import abspath

print ('####### SCRIPT START ##########')
#connect to the db

final_xml_path = "C:\\Users\\cabertra\\Documents\\PAE\\Hard Disk\\DE_Germany\\XMLS\\TSReader"
#final_xml_path = "C:/Users/cabertra/Documents/PAE/Hard Disk/DE_Germany/XMLS/TSReader/"

def ls(final_xml_path = getcwd()):
        #absolute xml path
        #return [abspath(arch.path) for arch in scandir(final_xml_path) if arch.is_file()]
        #only xml filename
        return [arch.name for arch in scandir(final_xml_path) if arch.is_file()]
xml_list = ls(final_xml_path)

for i in range (0,len(xml_list)):
        #print (xml_list[i])
        fullname = os.path.join(final_xml_path, xml_list[i])
        #fullname = final_xml_path + xml_list[i]

        print (fullname)

        tree = ET.parse(fullname)
        root = tree.getroot()
        print (root)

        #EXAMPLE OF USING TREE HIERARCHY TO GET THE CHILD WE WANT
        #print (root[11][2][0].text)

        #USING ELEMENT TO GET THE PID NUMBER AND DESCRIPTORS
        for pid_usage in root.findall('PID-USAGE'):
           for pid in pid_usage.findall('PID'):
                #I already cast the text of number to an hexadecimal number var
                number =  hex(int(pid.find('NUMBER').text,16))
                description = pid.find('DESCRIPTION').text
                print (number)
                print (description)
                print ('####')

print ('####### SCRIPT END ##########')