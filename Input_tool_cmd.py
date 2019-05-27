import os
import shutil
import sys
from time import sleep
import ntpath

from Input_tool_functions import check_name, check_duplicate, check_corrupted, check_encrypted, check_incomplete
import constants

def cmd_input(pathts, pathxml):
    
    ts = ntpath.basename(pathts)   
    xml = ntpath.basename(pathxml)
 
    # Check if the XML is already in the DATABASE    (Which path should go here???)
    if check_duplicate(constants.MERGED_XMLS_PATH, xml):
        print(xml+"is already in database please delete it in the folder")
        sys.exit(0)

    # Check if every TS has its matching xml
    if check_name(ts, xml):
        print("Please the xml and ts are not matching")
        sys.exit(0)

    # Check if xml is corrupted
    corrupt = check_corrupted(pathxml,xml,0)
    if corrupt == "1":
        print("The xml is corrupt: PAT is missing.")
    elif corrupt == "2":
        print("The xml is corrupt: PMT is missing.")
    elif corrupt == "3":
        print("Media is missing. Reparse.")
    elif corrupt == "4":
        print("The NewParser xml is OK.")
    elif corrupt == "5":
        print("The xml is blank or incorrect.")
    elif corrupt == "0":
        print("The xml is OK.")
    shutil.move(os.path.join(pathts, ts), os.path.join(os.path.normpath(constants.TS_PATH), ts))

    # RUN PARSER
    os.chdir(os.path.normpath(constants.PARSER_PATH))
    os.system(constants.RUN_PARSER)
    print("Parser")

    corrupt = check_corrupted(constants.NEWPARSER_PATH,xml,1)
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
    elif corrupt == "0":
        print ("The SA xml is OK.")

    # aquí hauriem de tornar a runnejar el nostre parser si ens diu que es corrupte

    if check_encrypted(constants.NEWPARSER_PATH, xml):
        print ('Congratulations. No encrypted tracks were found')
    else:
        print ('There are some encrypted tracks')
        sleep(1)

    # RUN MERGER
    print("Merger")
    os.chdir(os.path.normpath(constants.MERGER_PATH))
    os.system(constants.RUN_MERGER)

    missing_parameters_dict = {}

    missing_parameters_dict[xml] = check_incomplete(pathxml, xml)

    # RUN DATABASE
    shutil.move(os.path.join(pathxml,xml),os.path.join(os.path.normpath(constants.MERGED_XMLS_PATH),xml))
    print("DataBase")
    os.chdir(os.path.normpath(constants.DATABASE_PATH))

    if missing_parameters_dict[xml]:
        print(xml + " has the following missing parameters:")
        for missing_parameter in missing_parameters_dict[xml]:
            print(missing_parameter)
    while True:
        response = input("The xml is incomplete. Are you sure that you want to upload the TS anyways? (y/n)")
        if response in constants.YES:
            while True:
                response2 = input("This changes will be irreversible. Are you really sure? (y/n)")
                if response2 in constants.YES:
                    print('Running data miner')
                    os.system(constants.RUN_DATAMINER)
                    break
                elif response in constants.NO:
                    print('Process aborted')
                    break
            break

        elif response in constants.NO:
            print('Process aborted')
            break


