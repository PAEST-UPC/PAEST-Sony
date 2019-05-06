#This file implements the search by string feature.

import re,os

######## PRIVATE FUNCTIONS ########

# return True if a pattern is contained in a line
def _findLine(pattern,line):
    match = re.search(pattern,line)                 #Returns a match object if pattern is contained in line. If it doesn't match it returns a None object. 
    if match:                               
        return True
    return False
# return True if a pattern is contained in a File
def _findFile(pattern,filePath):            
    with open(filePath) as file:                    #Opens a file given by filePath. Doesn't need to be closed because of the with-as structure.
        for line in file:
            if _findLine(pattern,line):
                return True
    return False


######## PUBLIC FUNCTIONS ########

# return a list of all files in a directory (recursive for subdirectories) that contain a pattern
def searchText(pattern,dirPath):
    matchList = []                                  #Creates a list where all the files that contain the pattern will be saved.

    for fileName in os.listdir(dirPath):
        path = os.path.join(dirPath,fileName)       #Given a dirPath and a fileName creates a path.
        if os.path.isfile(path):                    #Checks if the path is a file.
            if _findFile(pattern,path):
                matchList.append(fileName)          #Appends the fileName to the matchList.
        elif os.path.isdir(path):                   #Checks if the path is a directory.
            matchList += searchText(pattern,path)   #Calls itself again until it finds a file.
    return matchList


