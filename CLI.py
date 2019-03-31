import argparse
from QueryModule import *
from SearchModule import *
import ast


# This function parses the arguments and returns a searchDict
def parseArguments(filterDict):
	searchDict = {}
	parser = argparse.ArgumentParser(description='Search for TS that match a criteria')
	for table_name, column_name in filterDict:
		parser.add_argument('--'+column_name)#, help=f'Filter by {column_name}. Current available options: {filterDict[(table_name,column_name)]}')
		
	args = vars(parser.parse_args())
	for table_name, column_name in filterDict:
		if args[column_name]:
			searchDict[(table_name,column_name)] = args[column_name]
	return searchDict


#filterDict = ast.literal_eval(open("filterDict2.txt", "r").read())
filterDict = obtainFilterDictMT()
searchDict = parseArguments(filterDict)
searchResult = querySearchMT(searchDict)
