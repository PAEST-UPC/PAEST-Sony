#! /usr/bin/python
import os

def del_extention(filename, lenght):
	return filename[0:len(filename)-lenght]

def comment_parser(filename, file_len, comment_pos, partes):
	counter=0
	if file_len>=comment_pos+1:
		comment=partes[comment_pos]
		for parte in partes:
			if counter>=comment_pos+1:
				comment+="_"+parte	
			counter+=1
	else:
		comment="none"
	return comment

def new_label(upper_element, tag, text, ET):
	new=ET.SubElement(upper_element, tag)
	if text!=None:
		new.text=text
	return new
	

def get_files(path):
	files= os.listdir(path)
	for filename in files:
	
		if os.stat(path+filename).st_size == 0:
			os.remove(path+filename)
			files.remove(filename)
			print(filename+ " has been deleted")
	return files	

def new_xml_file(path, tree):
	open(path, "w")
	tree.write(path)
