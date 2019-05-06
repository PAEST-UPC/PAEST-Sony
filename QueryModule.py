# Implements the functions that will interact with the DataBase.

import mysql.connector


# DB server variables
dbServerName = "127.0.0.1"
dbUser = "ubuntu"
dbPassword = "paesa19"
dbName = "searcherTest2"
dictdbName = "dictionary"
charSet = "utf8mb4"

######## PRIVATE FUNCTIONS ########

# Auxiliary private function that encapsulates queries to the DB.
def _queryDB(sqlQuery,dbName):
    # Create a connection object.
    connectionObject = mysql.connector.connect(host=dbServerName, user=dbUser, password=dbPassword,
                                         db=dbName, charset=charSet)
    try:
        # Create a cursor object.
        cursorObject = connectionObject.cursor()

        # Execute the sqlQuery.
        cursorObject.execute(sqlQuery)

        # Fetch all the rows.
        return cursorObject.fetchall()
    
    except Exception as e:
        # Prints the error if occured.
        print("Exception occured:{}".format(e))

    finally:
        # Always close the conection object.
        connectionObject.close()

# Auxiliary function that checks whether the column_name is a parameter that the user wants to filter by.
def _obtainIsFilter():
    # Creates an empty dictionary.
    isFilter = {}

    # Gets the information from Filters table
    sqlQuery = "SELECT * FROM Filters"
    rows = _queryDB(sqlQuery,dictdbName)
    
    # Iterates in rows and gets the useful parameters from use.
    for column_name, use in rows:
        isFilter[column_name] = use
    
    # Returns the parameters in the dictionary isFilter.
    return isFilter

# Auxiliary function that returns the tables information. 
def _obtainTables():

    # Obtain table_name, column_name, column_key of all columns in DB.
    sqlQuery = "SELECT table_name, column_name, column_key FROM information_schema.columns WHERE table_schema = '{0}' order by table_name".format(dbName)

    # Execute the sqlQuery and get answer.
    return _queryDB(sqlQuery,dbName)

# Function to obtain a dictionary to convert the values from the database to a user friendly ones.
def _obtainConversionDict():
    conversionDict = {}

    # Obtain table_name, column_name, value_name, UserFriendly_value of all columns in DB.
    sqlQuery = "SELECT type, var_obtained, value, meaning FROM Dictionary"
    rows = _queryDB(sqlQuery,dictdbName)
    # Iterates rows in order to convert the values to the user friendly ones.
    for table_name, column_name, value_name, userFriendly_value in rows:
        # Checks if the value is a digit, because SQL saves it as string and adds the "'" character.
        if value_name.strip("'").isdigit(): 
            conversionDict[(table_name,column_name,int(value_name.strip("'")))] = userFriendly_value
        else:
            conversionDict[(table_name,column_name,value_name)] = userFriendly_value
    # Returns the dictionary.
    return conversionDict

# Function that given a user friendly value, it returns the corresponding parameter in the database.
def _obtainInvConversionDict():
    invConversionDict = {}

    # Obtain table_name, column_name, value_name, UserFriendly_value of all columns in DB.
    sqlQuery = "SELECT type, var_obtained, value, meaning FROM Dictionary"
    rows = _queryDB(sqlQuery,dictdbName)
    for table_name, column_name, value_name, userFriendly_value in rows:
        if value_name.strip("'").isdigit():
            invConversionDict[userFriendly_value] = value_name.strip("'")
        else:
            invConversionDict[userFriendly_value] = value_name
    return invConversionDict

######## PUBLIC FUNCTIONS ########



# This function returns a dictionary containing all the fields and their corresponding values to search for.
def obtainFilterDict():
    
    # Obtain table information.
    tableInfo = _obtainTables()

    # Obtain isFilter dictionary.
    isFilter = _obtainIsFilter()

    # Obtain convertion dictionary.
    conversionDict = _obtainConversionDict()

    # Create dictionary to store db info.
    # Tuple of (Table,Column) as key and list of distinct values for the column as value.
    filterDict = {}
    for table_name, column_name, column_key in tableInfo:
        if isFilter[column_name]:
            sqlQuery = "SELECT distinct {0} FROM {1} order by {0}".format(column_name, table_name)
            values = _queryDB(sqlQuery,dbName)
            filterDict[(table_name,column_name)] = []
            for tupled_value in values:
                for value in tupled_value:
                    if (table_name,column_name,value) in conversionDict:
                        filterDict[(table_name,column_name)].append(conversionDict[(table_name,column_name,value)])
                    else:
                        filterDict[(table_name,column_name)].append(value)
    return filterDict

# This function makes the query to the database by obtaining the dictionary with the fields and corresponding values to search, chosen by the user.
def querySearch(searchDict, urlsFlag=False):
    
    conversionDict = _obtainConversionDict()
    invConversionDict = _obtainInvConversionDict()

    if not searchDict:
        return 'select something'
    else:

        sqlQuery = "SELECT idPMT FROM PMT WHERE "

        firstFlag = True
        for table_name, column_name in searchDict:
            if searchDict[(table_name,column_name)] in invConversionDict:
                    searchDict[(table_name,column_name)] = invConversionDict[searchDict[(table_name,column_name)]]

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
    
    # Execute the sqlQuery and get answer in rows.
    rows = _queryDB(sqlQuery,dbName)
    
    # Create dictionary to store result info.
    resultDict = {}

    # Dictionary format with urls: resultDict[Path][Service_Name] = [url1,url2,...].
    if urlsFlag:
        for Path, Service_Name, URL in rows:
            if ('PMT', 'Service_Name', Service_Name) in conversionDict:
                convertedService_Name = conversionDict[('PMT', 'Service_Name', Service_Name)]
            else:
                convertedService_Name = Service_Name
            if Path not in resultDict:
                resultDict[Path] = {}
            if Service_Name not in resultDict[Path]:
                resultDict[Path][convertedService_Name] = []
            resultDict[Path][convertedService_Name].append(URL)
    
    # Dictionary format without urls: resultDict[Path] = [Service_Name1,Service_Name2,...].
    else:
        for Path, Service_Name in rows:
            if Path not in resultDict:
                resultDict[Path] = []
            resultDict[Path].append(Service_Name)
    return resultDict
    