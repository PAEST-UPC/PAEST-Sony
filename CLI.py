import argparse, sys, pandas
from QueryModule import *
from SearchModule import *
import ast

filterDict = obtainFilterDictMT()
invConversionDict = obtainInvConversionDict()

def main():
    _xml_dir_path = r'/home/ubuntu/pae/xml/StreamAnalyzer'
    _searchString = False
    urlsFlag = None
    #filterDict = ast.literal_eval(open("filterDict2.txt", "r").read())
    filterDict = obtainFilterDictMT()
    conversionDict = obtainConversionDict()
    invConversionDict = obtainInvConversionDict()

    searchDict = _parseArguments(filterDict, conversionDict)
    if 'searchString' in searchDict:
        matchList = searchText(searchDict['searchString'],_xml_dir_path)
        return matchList
    else:
        searchResult = querySearchMT(searchDict,urlsFlag)
        df = pandas.DataFrame.from_dict(searchResult, orient='index')
        df.to_csv('test.csv')
        return searchResult

# This function parses the arguments and returns a searchDict
def _parseArguments(filterDict, conversionDict):
    searchDict = {}
    parser = argparse.ArgumentParser(description='Search for TS that match a criteria')
    for table_name, column_name in filterDict:
        convertedValues=[]
        for tupled_value in filterDict[(table_name, column_name)]:
            for value in tupled_value:
                if (table_name,column_name,value) in conversionDict:
                    convertedValues.append(conversionDict[(table_name,column_name,value)])
                else:
                    convertedValues.append(value)
        parser.add_argument('--'+column_name, help=f'Filter by {column_name}. Current available options: {convertedValues}')
    parser.add_argument('-s','--searchString',help='If you choose this option you can only filter by string, any other argument will cause an error')
    parser.add_argument('--getUrls', '-u', help='If you add this argument the results will include urls if possible', default=False, dest='getUrls', action='store_true')   
    
    if len(sys.argv)<2:
        parser.error('Missing arguments')

    args = vars(parser.parse_args())

    if args['searchString']:
        global _searchString
        _searchString = args['searchString']

        if len(sys.argv)>3:
            parser.error('searchString is not compatible with other arguments')
        else:
            searchDict['searchString'] = args['searchString']
        return searchDict   
    
    global urlsFlag
    urlsFlag = args['getUrls']

    for table_name, column_name in filterDict:
        if args[column_name]:
            if args[column_name] in invConversionDict:
                searchDict[(table_name,column_name)] = invConversionDict[args[column_name]]
            else:
                searchDict[(table_name,column_name)] = args[column_name]

    return searchDict

if __name__ == "__main__":
    result = main()
    print(result)