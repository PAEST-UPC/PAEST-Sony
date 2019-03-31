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

# return a list of all files in a directory that contain a pattern
def searchText(pattern,dirPath):
	matchList = []
	for filename in os.listdir(dirPath):
		if _findFile(pattern,os.path.join(dirPath,filename)):
			matchList.append(filename)
	return matchList

