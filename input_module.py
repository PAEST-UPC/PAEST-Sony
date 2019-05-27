import os
import shutil
import constants


def delete(xml_name):
    path_xml = os.path.join(constants.MERGED_XMLS_PATH, xml_name)
    if os.path.exists(path_xml):
        shutil.move(path_xml, constants.FLUSH_PATH)
        os.chdir(os.path.normpath(constants.DATABASE_PATH))
        os.system(constants.RUN_DATAMINER)
        return True
    else:
        return False


def flush():

    path = constants.FLUSH_PATH
    if os.path.exists(path):
        response = input("Are you sure you want to flush the tmp folder? (Y or N)")
        if response in constants.YES:
            response2 = input("This changes will be irreversible. Are you really sure? (Y or N)")
            if response2 in constants.YES:
                shutil.rmtree(path)
                os.mkdir(path)
            elif response in constants.NO:
                print('No files were deleted')
            else:
                print("WARNING: Temporary directory does not exists!")
            
        elif response in constants.NO:
            print("No files were deleted")
        else:
            print("Invalid answer. Please put Y or N")
    else:
        print("WARNING: Temporary directory does not exists!")
