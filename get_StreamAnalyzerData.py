#! /usr/bin/python
import xml.etree.ElementTree as ET
import os
import re
import merger_constants
from merger_functions import del_extention, comment_parser, new_label

path=merger_constants.INPUT_PATH_SA

def get_SA_data(filename):
		
	ET.register_namespace('', merger_constants.NAMESPACE_URL_SA)
	#ET.register_namespace('test', merger_constants.NAMESPACE_URL_NP)
	path=merger_constants.INPUT_PATH_SA
	tree=ET.parse(path+filename)
	root=tree.getroot()
	file_name=del_extention(filename, merger_constants.SA_EXTENTION_LEN)
	path_ts=merger_constants.TS_PATH+file_name+".ts"
	different_type=False
	
	title_parts=re.split("_",file_name)
	tipo=title_parts[merger_constants.TYPE_POS]

	if tipo=="T" or tipo=="T2":

		tipo_string="Terrestial"
		country=title_parts[merger_constants.T_COUNTRY_POS]
		frequency=title_parts[merger_constants.T_FREQUENCY_POS]
		comment=comment_parser(filename, len(title_parts), merger_constants.T_COMMENT_POS, title_parts )
											
	elif tipo=="C" or tipo=="C2":

		tipo_string="Cable"			
		country=title_parts[merger_constants.C_COUNTRY_POS]
		frequency=title_parts[merger_constants.C_FREQUENCY_POS]
		operator=title_parts[merger_constants.C_OPERATOR_POS]
		comment=comment_parser(filename, len(title_parts),merger_constants.C_COMMENT_POS, title_parts )
					
	elif tipo=="S" or tipo=="S2":
	
		tipo_string="Satellite"
		country="Satellite"
		frequency=title_parts[merger_constants.S_FREQUENCY_POS]
		orbit_pos=title_parts[merger_constants.S_ORBITPOS_POS]
		comment=comment_parser(filename, len(title_parts),merger_constants.S_COMMENT_POS, title_parts )			
		



	#creating labels	
	info_label=new_label(root,"Information", None, ET)
	country_label = new_label(info_label,'Country', country, ET)
	comment_label = new_label(info_label,'Comment', comment, ET)
	frequency_label = new_label(info_label,'Frequency', frequency, ET)
	path_label = new_label(info_label,'Path',path_ts, ET)
	type_label=new_label(info_label,"Type", tipo_string, ET)
	if tipo_string== "Cable":
		operator_label = new_label(info_label,'Operator', operator, ET)
	elif tipo_string=="Satellite":
		orbit_label=new_label(info_label,"Orbital_Position", orbit_pos, ET)

				
	return [tree, root]
