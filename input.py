#!python

import xml.etree.ElementTree as ET

print ('#################################')
tree = ET.parse('C_KBW_DE_Stuttgart_20130114_394MHz_256QAM_6900sym_SkyAktion_Guide-TSReader.xml')
root = tree.getroot()

print (root[11][2][0].text)
