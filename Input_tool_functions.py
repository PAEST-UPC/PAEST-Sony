import os
import xml.etree.ElementTree as ET
import constants


def check_incomplete(path, xml):

    tag ="{http://www.streamanalyser.com/schema}"

    text_out = []
    counter = 0
    
    path_xml = os.path.join(path, xml.strip(constants.SA_EXTENSION) + '.xml')

    try:
        e = ET.parse(path_xml)
        root = e.getroot()
        #TS TABLE
        inf1 = root.findall(tag+'Information')
        if inf1 == []:
            text_out.append("Information section")
            counter += 1

        for inf in root.findall(tag+'Information'):

            country_code = inf.find(tag+'Country').text
            comment = inf.find(tag+'Comment').text
            frequency = inf.find(tag+'Frequency').text
            path = inf.find(tag+'Path').text
            tipe = inf.find(tag+'Type').text
            if tipe == "Cable":
                operator = inf.find(tag+'Operator').text
                if operator == "-1":
                    text_out.append("operator")
                    counter = counter +1
            elif tipe == "Satellite":
                orbital_position = inf.find(tag+'Orbital_Position')
                if orbital_position == "-1":
                    text_out.append("orbital position")
                    counter = counter +1
            if country_code == "-1":
                text_out.append("country code")
                counter = counter +1
            if comment == "-1":
                text_out.append("comment")
                counter = counter +1
            if frequency == "-1":
                text_out.append("frequency")
                counter = counter +1
            if path == "-1":
                text_out.append("path")
                counter = counter +1
            if tipe == "-1":
                text_out.append("type")
                counter = counter +1



                # TS TABLE
        for tot in root.findall(tag+'TOT'):
            recording_time = tot.find(tag+'UTC_time')
            if recording_time == "-1":
                text_out.append("UTC_time")
                counter = counter +1

        # PMT TABLE
        for PMT in root.findall(tag+ 'PMT'):
            pid = int(PMT.find(tag+'PID').text,16)
            if pid == "-1":
                text_out.append("PID")
                counter = counter +1
            for child in root:
                if child.tag == (tag+'Onids'):
                    for onids in root.findall(tag+'Onids'):
                        for onid in onids.findall(tag+'Onid'):
                            onid_PID = int(onid.find(tag+'PID').text,16)
                            if onid_PID == pid:
                                num_onid = onid.find(tag+'Onid_Number').text
                                name_onid = onid.find(tag+'Onid_Operator').text
                                network_onid = onid.find(tag+'Onid_Network_Name').text
                                country_onid = onid.find(tag+'Onid_Country').text
                                if num_onid == "-1":
                                    text_out.append("Onid_Number")
                                    counter = counter +1
                                if name_onid == "-1":
                                    text_out.append("Onid_Operator")
                                    counter = counter +1
                                if network_onid == "-1":
                                    text_out.append("Onid_Network_Name")
                                    counter = counter +1
                                if country_onid == "-1":
                                    text_out.append("Onid_Country")
                                    counter = counter +1

            for streams in PMT.findall(tag+'Streams'):

                for stream in streams.findall(tag+'Stream'):
                    stream_type = int(stream.find(tag+'stream_type').text, 16)

                    elementary_PID = int(stream.find(tag+'elementary_PID').text, 16)
                    for streamIdDescriptor in stream.findall(tag+'StreamIdentifierDescriptor'):
                        component_tag = streamIdDescriptor.find(tag+'component_tag')
                        if component_tag == "-1":
                            text_out.append(("Component_tag. PID:" + str(pid)))
                            counter = counter +1
                    if stream_type == "-1":
                        text_out.append((" Stream_type. PID:" + str(pid)))
                        counter = counter +1
                    if elementary_PID == "-1":
                        text_out.append((" Stream elementary_PID. PID:" + str(pid)))
                        counter = counter +1

                    # AUDIO TABLE

                    if stream_type == constants.AUDIO_MPEG_1 or stream_type == constants.AUDIO_MPEG_2 or stream_type == constants.AUDIO_MPEG4_AAC or stream_type == constants.AUDIO_MPEG_AAC or stream_type == constants.AUDIO_AC3 or stream_type == constants.AUDIO_DTS:
                        for languageDescriptor in stream.findall(tag+'ISO639LanguageDescriptor'):
                            for language in languageDescriptor.findall(tag+'Language'):
                                audio_language = language.find(tag+'ISO_639_language_code').text
                                audio_type = language.find(tag+'audio_type').text
                                if audio_language == "-1":
                                    text_out.append(("Audio language. PID:" + str(pid)+  ". Stream's elementary PID:" + str(elementary_PID)))
                                    counter = counter +1
                                if audio_type == "-1":
                                    text_out.append(("Audio type. PID:" + str(pid)+  ". Stream's elementary PID:" + str(elementary_PID)))
                                    counter =counter +1
                    elif stream_type == constants.TEXT:
                        # DATA SECTION
                        for child in stream:
                            # SUBTITLES SECTION
                            if child.tag == (tag+'SubtitlingDescriptor'):
                                for subDescriptor in stream.findall(tag+'SubtitlingDescriptor'):
                                    for subtitle in subDescriptor.findall(tag+'Subtitle'):
                                        subtitle_language = subtitle.find(tag+'ISO_639_language_code').text
                                        if subtitle_language == "-1":
                                            text_out.append(("ISO_639_language_code in subtitles section. PID:" + str(pid)+  ". Stream's elementary PID:" + str(elementary_PID)))
                                            counter = counter +1
                            # TELETEXT SECTION
                            if child.tag == (tag+'TeletextDescriptor'):
                                for teletextDescriptor in stream.findall(tag+'TeletextDescriptor'):
                                    for teletext in teletextDescriptor.findall(tag+'Teletext'):
                                        teletext_language = teletext.find(tag+'ISO_639_language_code').text
                                        if teletext_language == "-1":
                                            text_out.append(("ISO_639_language_code in teletext section. PID:" + str(pid)+  ". Stream's elementary PID:" + str(elementary_PID)))
                                            counter = counter +1
                    elif stream_type == constants.PRIVATE:
                        for child in root:
                            if child.tag == (tag+'AIT'):
                                for ait in root.findall(tag+'AIT'):
                                    private_pid = int(ait.find(tag+'PID').text,16)
                                    if private_pid == elementary_PID:
                                        for apps in ait.findall(tag+'Applications'):
                                            for app in apps.findall(tag+'Application'):
                                                for transportDescriptor in app.findall(tag+'TransportProtocolDescriptor'):
                                                    for urls in transportDescriptor.findall(tag+'URLs'):
                                                        for urlFinal in urls.findall(tag+'URL'):
                                                            for urlList in  urlFinal.findall(tag+'URLBase'):
                                                                url = urlList.text
                                                            if url == "-1":
                                                                text_out.append(("URLBase. PID:" + str(pid)+  ". Stream's elementary PID:" + str(elementary_PID)))
                                                                counter = counter +1




        # VIDEO TABLE
        video_section = root.findall(tag+'Video')
        if video_section == []:
            text_out.append("Video section")
            counter = counter +1
        for video in root.findall(tag+'Video'):
            video_typename = video.find(tag+'TypeName').text
            for info in video.findall(tag+'Info'):
                height = info.find(tag+'Height').text
                width = info.find(tag+'Width').text
                interlaced=info.find(tag+'Interlaced').text
            if video_typename == "-1":
                text_out.append("Video typename")
                counter = counter +1
            if height == "-1":
                text_out.append("Video height")
                counter = counter +1
            if width == "-1":
                text_out.append("Video width")
                counter = counter +1
            if interlaced == "-1":
                text_out.append("Interlaced")
                counter = counter +1

        for parserInfo in root.findall(tag+'Parser_Info'):
            for vids in parserInfo.findall(tag+'Videos'):
                for vid in vids.findall(tag+'Video'):
                    identifierVid = int(vid.find(tag+'ID').text)
                    width = vid.find(tag+'Width').text
                    height = vid.find(tag+'Height').text
                    bit_rate_mode = vid.find(tag+'BitRate_Mode').text
                    pixel_aspect_ratio = vid.find(tag+'PixelAspectRatio').text
                    display_aspect_ratio = vid.find(tag+'DisplayAspectRatio').text
                    frame_rate = vid.find(tag+'FrameRate').text
                    if width == "-1":
                        text_out.append(("Video Width. ID: " + str(identifierVid)))
                        counter = counter +1
                    if height == "-1":
                        text_out.append(("Video Height. ID: " + str(identifierVid)))
                        counter = counter +1
                    if bit_rate_mode == "-1":
                        text_out.append(("Video BitRate_Mode. ID: " + str(identifierVid)))
                        counter = counter +1
                    if pixel_aspect_ratio == "-1":
                        text_out.append(("Video PixelAspectRatio. ID: " + str(identifierVid)))
                        counter = counter +1
                    if display_aspect_ratio == "-1":
                        text_out.append(("Video DisplayAspectRatio. ID: " + str(identifierVid)))
                        counter = counter +1
                    if frame_rate == "-1":
                        text_out.append(("Video FrameRate. ID: " + str(identifierVid)))
                        counter = counter +1



        for parserInfo in root.findall(tag+'Parser_Info'):
            for auds in parserInfo.findall(tag+'Audios'):
                for aud in auds.findall(tag+'Audio'):
                    identifierVid = int(aud.find(tag+'ID').text)
                    bit_rate_mode = aud.find(tag+'BitRate_Mode').text
                    bit_rate = float(aud.find(tag+'BitRate').text)
                    channels = aud.find(tag+'Channels').text
                    frame_rate = float(aud.find(tag+'FrameRate').text)
                    if bit_rate_mode == "-1":
                        text_out.append(("Audio BitRate_Mode. ID: " + str(identifierVid)))
                        counter = counter +1
                    if bit_rate == "-1":
                        text_out.append(("Audio BitRate. ID: " + str(identifierVid)))
                        counter = counter +1
                    if channels == "-1":
                        text_out.append(("Audio Channels. ID: " + str(identifierVid)))
                        counter = counter +1
                    if frame_rate == "-1":
                        text_out.append(("Audio FrameRate. ID: " + str(identifierVid)))
                        counter = counter +1

    except ET.ParseError:
        print("XML completely empty.")
        pass

    finally:
        if counter >0:
            return text_out


def check_name(ts, xml):

    ts = ts.strip('.ts')
    xml = xml.strip(constants.SA_EXTENSION)
    if ts == xml:
        #TS i XML match
        return True
    else:
        #TS i XML no match
        return False


def check_encrypted(path, xml):
    #This tag is necessary, as (idk why) it preceeds every tag in all tags of xml
    #this means that instead of <Encryption> we would find {tag}{encryption}#
    #We can see it by printing media.tag for example in line 24#
    tag ="{https://mediaarea.net/mediainfo}"
    if constants.SA_EXTENSION in xml:
        xml = xml.strip(constants.SA_EXTENSION)
        xml += ".xml" 
    
    path_xml = os.path.join(path,xml)  

    #We parse the file passed as a parameter#
    arxiu_a_comprobar = ET.parse(path_xml)
    #Get the root tag
    root = arxiu_a_comprobar.getroot()
    #number of encrypted tags we will find
    counter = 0
    #for every track contained in every media, we look for all Encrypted Tags#
    for media in root.findall(tag+'media'):
        for track in media.findall(tag+'track'):
            for enc in track.findall(tag+'Encryption'):
                counter = counter+1
                #print(enc.text) text of the tag <Encryption> (do not delete)
    #if any encrypted tags were found:#
    if counter>0:
        return False
    else:
        return True


def check_duplicate(path,xml):
    #This is the path of the directory which contains the xml that the#
    #merger has output#
    
    #this only gets the name of a file that one passes as a parameter#

    #This retrieves all the names of the files of the directory where are
    #all the xml's of the merger output#
    def ls(path = os.getcwd()):
        return [arch.name for arch in os.scandir(path) if arch.is_file()]
    xml_list = ls(path)
    print(xml_list)
    print(xml)
    #Compares, one by one, the name of our under test xml with
    #the names of the xml on the list, which are in the database.
    if xml.strip(constants.SA_EXTENSION)+ constants.DEFAULT_EXTENTION in xml_list:
            return True

    return False


def check_corrupted(path, xml, tag):
    try:
        
        path_xml = os.path.join(path, xml) 
        e = ET.parse(path_xml)
        root = e.getroot()

        if(tag == '0'):
            tag = "{http://www.streamanalyser.com/schema}"
            var1 = root.findall(tag+'PAT')
            var2 = root.findall(tag+'PMT')

            if (var1 == []):
                return ("1")
            elif (var2==[]):
                return ("2")
            else:
                return ("0")
        else:
            tag = "{https://mediaarea.net/mediainfo}"
            var = root.findall(tag+'media')

            if (var == []):
                return ("3")
            else:
                return ("4")

    except:
        return ("5")
