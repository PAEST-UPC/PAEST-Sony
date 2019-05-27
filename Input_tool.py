#!/usr/bin/env python


import os
import shutil
import sys
from time import sleep
from Input_tool_functions import check_name, check_duplicate, check_corrupted, check_encrypted, check_incomplete
import constants


def input_tool(ignoreErrors, automatize):
    if not ignoreErrors:
        counter = 0
        ts_list = []
        xml_list = []
        path = os.path.normpath(constants.INPUT_PATH)
        files = os.listdir(path)



        for filename in files:
            if filename.endswith(".xml"):
                xml_list.append(filename)
            else:
                ts_list.append(filename)

        if not (ts_list or xml_list):
            print (ts_list)
            print (xml_list)
            print ('Input folder empty')
            sys.exit(0)

        # Check if the XML is already in the DATABASE
        for xml in xml_list:
            if check_duplicate(constants.MERGED_XMLS_PATH, xml):
                print(xml+" is already in database please delete it in the folder")
                sys.exit(0)

        # Check if every TS has its matching xml
        for ts in ts_list:
            for xml in xml_list:
                if check_name(ts,xml):
                    counter+=1

        if not (ts_list) or not (xml_list):
            print (ts_list)
            print (xml_list)
            print ('Input folder empty')
            sys.exit(0)

        if len(ts_list) != counter:
            print("Please there is an xml and a ts that are not matching in the folder")
            sys.exit(0)



        # Check if xml is corrupted
        for xml in xml_list:
            corrupt = ""
            corrupt = check_corrupted(constants.INPUT_PATH,xml,0)
            if corrupt == "1":
                print("The xml is corrupt: PAT is missing.")
            elif corrupt == "2":
                print("The xml is corrupt: PMT is missing.")
            elif corrupt == "3":
                print("Media is missing. Reparse.")
            elif corrupt == "4":
                print("The NewParser xml is OK.")
            elif corrupt == "5":
                print ("The xml is blank or incorrect.")
                sys.exit(0)
            elif corrupt == "0":
                print ("The SA xml is OK.")

        for ts in ts_list:
            shutil.move(os.path.join(path,ts),os.path.join(os.path.normpath(constants.TS_PATH),ts))

            #RUN PARSER
        os.chdir(os.path.normpath(constants.PARSER_PATH))
        os.system(constants.RUN_PARSER)

        for xml in xml_list:
            corrupt = check_corrupted(constants.NEWPARSER_PATH, xml, 1)
            corrupted_dict = {
                'PAT_missing' : [],
                'PMT_missing' : [],
                'Media_missing' : [],
                'NewParser_correct' : [],
                'Incorrect' : [],
                'StreamAnalyzer_correct' : []
            }

            if corrupt == "1":
                corrupted_dict['PAT_missing'].append(xml)
            elif corrupt == "2":
                corrupted_dict['PMT_missing'].append(xml)
            elif corrupt == "3":
                corrupted_dict['Media_missing'].append(xml)
            elif corrupt == "4":
                corrupted_dict['NewParser_correct'].append(xml)
            elif corrupt == "5":
                corrupted_dict['Incorrect'].append(xml)
            elif corrupt == "0":
                corrupted_dict['StreamAnalyzer_correct'].append(xml)

            encrypted_dict = {'encrypted' : [], 'non_encrypted' : []}
            if check_encrypted(constants.NEWPARSER_PATH, xml):
                encrypted_dict['non_encrypted'].append(xml)
            else:
                encrypted_dict['encrypted'].append(xml)

            shutil.move(os.path.join(path, xml), os.path.join(os.path.normpath(constants.INPUT_PATH_SA), xml))


        #RUN MERGER
        os.chdir(os.path.normpath(constants.MERGER_PATH))
        os.system(constants.RUN_MERGER)

        missing_parameters_dict = {}
        for xml in xml_list:
            missing_parameters_dict[xml] = check_incomplete(constants.MERGED_XMLS_PATH, xml)

        #RUN DATABASE
        os.chdir(os.path.normpath(constants.DATABASE_PATH))

        print('Corrupted info:')
        for corruption_type in corrupted_dict:
            print(corruption_type + ':')
            for xml in corrupted_dict[corruption_type]:
                print(xml)

        print('Encrypted info:')
        for xml in encrypted_dict['encrypted']:
            print(xml)

        for xml in xml_list:

            if missing_parameters_dict[xml]:
                print(xml + " has the following missing parameters:")
                for missing_parameter in missing_parameters_dict[xml]:
                    print(missing_parameter)

        if not automatize:

            while True:
                response = input("There are some incomplete xml files. Are you sure that you want to upload the TS's anyways? (y/n)")
                if response in constants.YES:
                    while True:
                        response2 = input("This changes will be irreversible. Are you really sure? (y/n)")
                        if response2 in constants.YES:
                            print('Running data miner')
                            os.system(constants.RUN_DATAMINER)
                            break
                        elif response in constants.NO:
                            print('Process aborted')
                            sys.exit(0)
                            break
                    break

                elif response in constants.NO:
                    print('Process aborted')
                    sys.exit(0)
                    break
        else:
            os.system(constants.RUN_DATAMINER)

    else:
        os.chdir(os.path.normpath(constants.PARSER_PATH))
        os.system(constants.RUN_PARSER)
        os.chdir(os.path.normpath(constants.MERGER_PATH))
        os.system(constants.RUN_MERGER)
        os.chdir(os.path.normpath(constants.DATABASE_PATH))
        os.system(constants.RUN_DATAMINER)



