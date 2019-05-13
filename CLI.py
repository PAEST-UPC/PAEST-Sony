import argparse, sys, pandas, ast, os, time
from QueryModule import *
from SearchModule import *

CACHE_TIME = 3600

def main():
    start = time.time()
    _xml_dir_path = r'/home/ubuntu/pae/xml/Test9920'
    filterDict = getFilterDict()

    searchDict, urlsFlag, csvFlag = _parseArguments(filterDict)
    if 'searchString' in searchDict:
        matchList = searchText(searchDict['searchString'],_xml_dir_path)
        return matchList
    else:
        onlyTS = all([table_name == 'TS' for table_name, column_name in searchDict])
        searchResult = querySearch(searchDict,urlsFlag)
        
        if urlsFlag:
            for path in searchResult:
                print(path + ':')
                for service in searchResult[path]:
                    print(' ' + service + ': ')
                    for url in searchResult[path][service]:
                        print('     ' + url)
        else:
            for path in searchResult:
                if onlyTS:
                    searchResult[path] = 'All services'
                print(path + ': ' + str(searchResult[path]))

        if csvFlag:
            df = pandas.DataFrame.from_dict(searchResult, orient='index')
            df.to_csv('searchResult.csv')

    end = time.time()
    print(end-start)


# This function parses the arguments and returns a searchDict.
def _parseArguments(filterDict):
    searchDict = {}
    
    # Defines and describes the arguments of the helper.
    parser = argparse.ArgumentParser(description='Search for TS that match a criteria')
    for table_name, column_name in filterDict:
        parser.add_argument('--'+column_name, help=f'Filter by {column_name}. Current available options: {filterDict[(table_name,column_name)]}')
    parser.add_argument('-s','--searchString',help='If you choose this option you can only filter by string, any other argument will cause an error')
    parser.add_argument('--getUrls', '-u', help='If you add this argument the results will include urls if possible', default=False, dest='getUrls', action='store_true')   
    parser.add_argument('--exportCsv', '-csv', help='If you add this argument the results will be exported to a csv file', default=False, dest='exportCsv', action='store_true')   
    
    # Checks if there are arguments to search. If there aren't any returns error.
    if len(sys.argv) < 2:
        parser.error('Missing arguments')
        
    # If there is only one argument and no value to search returns all possible values for that argument.
    if len(sys.argv) == 2:
        for table_name, column_name in filterDict:
            if sys.argv[1] == '--'+column_name:
                parser.exit(message='Values of ' + column_name + ': ' + str(filterDict[(table_name,column_name)]))

    args = vars(parser.parse_args())

    urlsFlag = args['getUrls']

    csvFlag = args['exportCsv']

    if args['searchString']:
        if len(sys.argv)>3:
            parser.error('searchString is not compatible with other arguments')
        else:
            searchDict['searchString'] = args['searchString']
        return searchDict, urlsFlag, csvFlag

    for table_name, column_name in filterDict:
        if args[column_name]:
            searchDict[(table_name,column_name)] = args[column_name]

    return searchDict, urlsFlag, csvFlag
    
# This function creates a .txt file where the filters are saved as a cache to save unnecessary updates to database.
def getFilterDict():
    filename = 'filterDict.txt'
    filterDict = {}
    # Checks if the path contains the file.
    if os.path.isfile(filename):
        # Calculates the file time by calculating time.time() that returns the time in seconds since the epoch, and substracts the time of last modification of file with os.path.getmtime(filename.)
        file_time=time.time() - os.path.getmtime(filename)
        # Checks how old is the file. 
        if file_time < CACHE_TIME:
            # Opens a file given by filename in read mode. Doesn't need to be closed because of the with-as structure.
            with open(filename, "r") as data:
                filterDict = ast.literal_eval(data.read())
            return filterDict
    
    # In case that the time exceeds CACHE_TIME obtains the latest filter dictionary and overwrites the old one.
    filterDict = obtainFilterDict()
    with open(filename, "w") as file:
        file.write(str(filterDict))

    return filterDict

if __name__ == "__main__":
    main()