#! /usr/bin/python
import xml.etree.ElementTree as ET
import merger_constants

def get_NP_data(filename):

	root=ET.parse(merger_constants.INPUT_PATH_NP+filename).getroot()
	parser_info_label=ET.SubElement(root,"Parser_Info")
	videos_label=ET.SubElement(parser_info_label,"Videos")
	audios_label=ET.SubElement(parser_info_label,"Audios")
	for service in root.iter("{"+merger_constants.NAMESPACE_URL_NP+"}track"):
		if service.attrib["type"]=="Video":
			video_label=ET.SubElement(videos_label,"Video")
			
			for label in merger_constants.VIDEO_LABELS:
				
				new_label=service.find("{"+merger_constants.NAMESPACE_URL_NP+"}"+label)
				if new_label is not None:
					new_label.tag=new_label.tag.replace("{"+merger_constants.NAMESPACE_URL_NP+"}", '')
					video_label.append(new_label)
				

		elif service.attrib["type"]=="Audio":
			audio_label=ET.SubElement(audios_label,"Audio")
			
			for label in merger_constants.AUDIO_LABELS:	
				new_label=service.find("{"+merger_constants.NAMESPACE_URL_NP+"}"+label)
				if new_label is not None:
					if new_label.tag == "{"+merger_constants.NAMESPACE_URL_NP+"}"+"Channels":
						if new_label.text=="1":
							new_label.text="Mono"
						elif new_label.text=="2":
							new_label.text="Stereo"	
					new_label.tag=new_label.tag.replace("{"+merger_constants.NAMESPACE_URL_NP+"}", '')			
					audio_label.append(new_label)

	return parser_info_label
