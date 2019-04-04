#! /usr/bin/python
from merger_functions import get_files, del_extention, new_xml_file
from get_NewParserData import get_NP_data
from get_StreamAnalyzerData import get_SA_data
import merger_constants

sa_files=get_files(merger_constants.INPUT_PATH_SA)
np_files=get_files(merger_constants.INPUT_PATH_NP)
np_files_no_extention=[]
print(sa_files)
for filename in np_files:
	np_files_no_extention.append(del_extention(filename, merger_constants.NP_EXTENTION_LEN))

for filename in sa_files:
	std_filename=del_extention(filename, merger_constants.SA_EXTENTION_LEN)
	if std_filename+merger_constants.NP_EXTENTION in np_files:
		tree_root_sa=get_SA_data(filename)
		np_info_label=get_NP_data(std_filename+merger_constants.NP_EXTENTION)
		#for child in np_info_label.iter():
			#print(child.tag)
		tree_root_sa[1].append(np_info_label)
		print("Creating new merged xml for " +std_filename+merger_constants.DEFAULT_EXTENTION)
		new_xml_file(merger_constants.OUTPUT_PATH+std_filename+merger_constants.DEFAULT_EXTENTION,tree_root_sa[0])
	else:
		tree_root_sa=get_SA_data(filename)
		print("Creating new xml for " +std_filename+merger_constants.DEFAULT_EXTENTION)
		new_xml_file(merger_constants.OUTPUT_PATH+std_filename+merger_constants.DEFAULT_EXTENTION,tree_root_sa[0])
		
		
		
