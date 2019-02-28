#!python

import xml.etree.ElementTree as ET

print ('####### SCRIPT START ##########')
tree = ET.parse('C_KBW_DE_Stuttgart_20130114_394MHz_256QAM_6900sym_SkyAktion_Guide-TSReader.xml')
#we need to contemplate the way to get the names of the xml files for the ET.parse
root = tree.getroot()

#EXAMPLE OF USING TREE HIERARCHY TO GET THE CHILD WE WANT
print (root[11][2][0].text)

#USING ELEMENT TO GET THE PID NUMBER AND DESCRIPTORS
for pid_usage in root.findall('PID-USAGE'):
    for pid in pid_usage.findall('PID'):
        number = hex(pid.find('NUMBER').text)
        description = pid.find('DESCRIPTION').text
        print (number)
        print (description)
        print ('####')
        #here we need to call the function that inputs data to the database for each number and description


print ('####### SCRIPT END ##########')