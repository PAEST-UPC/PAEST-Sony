import argparse, sys, pandas
from QueryModule import *
from SearchModule import *
import ast

def main():
    _xml_dir_path = r'/home/ubuntu/pae/xml/StreamAnalyzer'
    _searchString = False
    urlsFlag = None
    csvFlag = None
    filterDict = obtainFilterDict()
    conversionDict = obtainConversionDict()
    invConversionDict = obtainInvConversionDict()

    searchDict = _parseArguments(filterDict, conversionDict, invConversionDict)
    if 'searchString' in searchDict:
        matchList = searchText(searchDict['searchString'],_xml_dir_path)
        return matchList
    else:
        onlyTS = all([table_name == 'TS' for table_name, column_name in searchDict])
        searchResult = querySearch(searchDict,urlsFlag)
        
        for path in searchResult:
            if onlyTS:
                searchResult[path] = 'All services'
            print(path + ': ' + str(searchResult[path]))

        if csvFlag:
            df = pandas.DataFrame.from_dict(searchResult, orient='index')
            df.to_csv('searchResult.csv')


# This function parses the arguments and returns a searchDict
def _parseArguments(filterDict, conversionDict, invConversionDict):
    searchDict = {}
    convertedValues = {}
    parser = argparse.ArgumentParser(description='Search for TS that match a criteria')
    for table_name, column_name in filterDict:
        convertedValues[column_name] = []
        for tupled_value in filterDict[(table_name, column_name)]:
            for value in tupled_value:
                if (table_name,column_name,value) in conversionDict:
                    convertedValues[column_name].append(conversionDict[(table_name,column_name,value)])
                else:
                    convertedValues[column_name].append(value)
        parser.add_argument('--'+column_name, help=f'Filter by {column_name}. Current available options: {convertedValues[column_name]}')
    parser.add_argument('-s','--searchString',help='If you choose this option you can only filter by string, any other argument will cause an error')
    parser.add_argument('--getUrls', '-u', help='If you add this argument the results will include urls if possible', default=False, dest='getUrls', action='store_true')   
    parser.add_argument('--exportCsv', '-csv', help='If you add this argument the results will be exported to a csv file', default=False, dest='exportCsv', action='store_true')   
    
    if len(sys.argv) < 2:
        parser.error('Missing arguments')
    if len(sys.argv) == 2:
        for table_name, column_name in filterDict:
            if sys.argv[1] == '--'+column_name:
                parser.exit(message='Values of ' + column_name + ': ' + str(convertedValues[column_name]))

    



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

    global csvFlag
    csvFlag = args['exportCsv']

    for table_name, column_name in filterDict:
        if args[column_name]:
            if args[column_name] in invConversionDict:
                searchDict[(table_name,column_name)] = invConversionDict[args[column_name]]
            else:
                searchDict[(table_name,column_name)] = args[column_name]

    return searchDict

if __name__ == "__main__":
    main()
    
