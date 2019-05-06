#Implements the functions that will interact with the DataBase

import mysql.connector


# DB server variables
dbServerName = "127.0.0.1"
dbUser = "ubuntu"
dbPassword = "paesa19"
dbName = "searcherTest2"
dictdbName = "dictionary"
charSet = "utf8mb4"

######## PRIVATE FUNCTIONS ########

# Auxiliary private function that encapsulates queries to the DB
def _queryDB(sqlQuery,dbName):
    # Create a connection object
    connectionObject = mysql.connector.connect(host=dbServerName, user=dbUser, password=dbPassword,
                                         db=dbName, charset=charSet)
    try:
        # Create a cursor object
        cursorObject = connectionObject.cursor()

        # Execute the sqlQuery
        cursorObject.execute(sqlQuery)

        # Fetch all the rows
        return cursorObject.fetchall()
    
    except Exception as e:
        #Prints the error if occured
        print("Exception occured:{}".format(e))

    finally:
        #Always close the conection object
        connectionObject.close()

#Auxiliary function that checks whether the column_name is a parameter that the user wants to filter by.
def _obtainIsFilter():
    #Creates an empty dictionary
    isFilter = {}

    #Gets the information from Filters table
    sqlQuery = "SELECT * FROM Filters"
    rows = _queryDB(sqlQuery,dictdbName)
    
    #Iterates in rows 
    for column_name, use in rows:
        isFilter[column_name] = use

    return isFilter

# Auxiliary function that returns
def _obtainTables():

    # Obtain table_name, column_name, column_key of all columns in DB
    sqlQuery = "SELECT table_name, column_name, column_key FROM information_schema.columns WHERE table_schema = '{0}' order by table_name".format(dbName)

    # Execute the sqlQuery and get answer
    return _queryDB(sqlQuery,dbName)

######## PUBLIC FUNCTIONS ########

def obtainConversionDict():
    conversionDict = {}

    # Obtain table_name, column_name, value_name, UserFriendly_value of all columns in DB
    sqlQuery = "SELECT type, var_obtained, value, meaning FROM Dictionary"
    rows = _queryDB(sqlQuery,dictdbName)
    for table_name, column_name, value_name, userFriendly_value in rows:
        if value_name.strip("'").isdigit(): 
            conversionDict[(table_name,column_name,int(value_name.strip("'")))] = userFriendly_value
        else:
            conversionDict[(table_name,column_name,value_name)] = userFriendly_value

    return conversionDict

def obtainInvConversionDict():

    invConversionDict = {}

    # Obtain table_name, column_name, value_name, UserFriendly_value of all columns in DB

    sqlQuery = "SELECT type, var_obtained, value, meaning FROM Dictionary"

    rows = _queryDB(sqlQuery,dictdbName)

    for table_name, column_name, value_name, userFriendly_value in rows:

        if value_name.strip("'").isdigit():

            invConversionDict[userFriendly_value] = value_name.strip("'")

        else:

            invConversionDict[userFriendly_value] = value_name

    return invConversionDict

# This function returns a dictionary containing all the needed info to start the GUI from MultiTable DB
def obtainFilterDict():
    
    # Obtain PKInfo()
    tableInfo = _obtainTables()

    # Obtain isFilter dictionary
    isFilter = _obtainIsFilter()

    # Create dictionary to store db info
    # Tuple of (Table,Column) as key and list of distinct values for the column as value
    filterDict = {}
    for table_name, column_name, column_key in tableInfo:
        if isFilter[column_name]:
            sqlQuery = "SELECT distinct {0} FROM {1} order by {0}".format(column_name, table_name)
            filterDict[(table_name,column_name)] = _queryDB(sqlQuery,dbName)
    del filterDict[('URL','URL')]
    return filterDict


def querySearch(searchDict, urlsFlag=False):
    if not searchDict:
        return 'select something'
    else:
        sqlQuery = "SELECT idPMT FROM PMT WHERE "

        firstFlag = True
        for table_name, column_name in searchDict:
            if not firstFlag:
                sqlQuery += " AND "
            
            if searchDict[(table_name,column_name)].isdigit():
                value = searchDict[(table_name,column_name)]
            else:
                value = "\'{0}\'".format(searchDict[(table_name,column_name)])

            if table_name == 'TS':
                sqlQuery += "identifierTS IN (SELECT identifierTS FROM PMT NATURAL JOIN TS WHERE {0}={1})".format(column_name,value)
            elif table_name == 'PMT':
                sqlQuery += "{0}={1})".format(column_name,value)
            elif table_name == 'Stream':
                sqlQuery += "idPMT IN (SELECT idPMT FROM Stream WHERE {0}={1})".format(column_name,value)
            else:
                sqlQuery += "idPMT IN (SELECT idPMT FROM Stream NATURAL JOIN {2} WHERE {0}={1})".format(column_name,value,table_name)
            firstFlag = False
    
    if urlsFlag:
        sqlQuery = "SELECT Path, Service_Name, URL FROM TS NATURAL JOIN (PMT NATURAL JOIN (Stream NATURAL JOIN (Private NATURAL JOIN URL))) WHERE idPMT IN ({0}) AND HbbTV=1".format(sqlQuery)
    else:
        sqlQuery = "SELECT Path, Service_Name FROM PMT NATURAL JOIN TS WHERE idPMT IN ({0})".format(sqlQuery)
    
    # Execute the sqlQuery and get answer in rows
    rows = _queryDB(sqlQuery,dbName)
    
    # Create dictionary to store result info
    resultDict = {}

    # Dictionary format with urls: resultDict[identifierTS][Service_Name] = [url1,url2,...]
    if urlsFlag:
        for Path, Service_Name, URL in rows:
            if Path not in resultDict:
                resultDict[Path] = {}
            if Service_Name not in resultDict[Path]:
                resultDict[Path][Service_Name] = []
            resultDict[Path][Service_Name].append(URL)
    
    # Dictionary format without urls: resultDict[Path] = [Service_Name1,Service_Name2,...]
    else:
        for Path, Service_Name in rows:
            if Path not in resultDict:
                resultDict[Path] = []
            resultDict[Path].append(Service_Name)
    return resultDict
    