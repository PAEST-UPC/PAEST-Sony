import re,os

######## PRIVATE FUNCTIONS ########

# return True if a pattern is contained in a line
def _findLine(pattern,line):
    match = re.search(pattern,line)
    if match:
        return True
    return False
# return True if a pattern is contained in a File
def _findFile(pattern,filePath):
    with open(filePath) as file:
        for line in file:
            if _findLine(pattern,line):
                return True
    return False


######## PUBLIC FUNCTIONS ########

# return a list of all files in a directory (recursive for subdirectorie) that contain a pattern
def searchText(pattern,dirPath):
    matchList = []

    for filename in os.listdir(dirPath):
        path = os.path.join(dirPath,filename)
        if os.path.isfile(path):
            if _findFile(pattern,path):
                matchList.append(filename)
        elif os.path.isdir(path):
            matchList += searchText(pattern,path)
    return matchList


