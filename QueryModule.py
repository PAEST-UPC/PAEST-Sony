# Implements the functions that will interact with the DataBase.

import mysql.connector

# DB server variables
dbServerName = "127.0.0.1"
dbUser = "ubuntu"
dbPassword = "paesa19"
dbName = "test9920"
dictdbName = "dictionary"
charSet = "utf8mb4"

# Constants
NOT_DEFINED = 'not defined'

######## PRIVATE FUNCTIONS ########


# Auxiliary private function that encapsulates queries to the DB.
def _query_db(sqlQuery, dbName):
    # Create a connection object.
    connection_object = mysql.connector.connect(host=dbServerName, user=dbUser, password=dbPassword,
                                                db=dbName, charset=charSet)
    try:
        # Create a cursor object.
        cursorObject = connection_object.cursor()

        # Execute the sqlQuery.
        cursorObject.execute(sqlQuery)

        # Fetch all the rows.
        return cursorObject.fetchall()

    except Exception as e:
        # Prints the error if occurred.
        print("Exception occured:{}".format(e))

    finally:
        # Always close the connection object.
        connection_object.close()


# Auxiliary function that checks whether the column_name is a parameter that the user wants to filter by.
def _obtainIsFilter():
    # Creates an empty dictionary.
    is_filter = {}

    # Gets the information from Filters table
    sql_query = "SELECT * FROM Filters"
    rows = _query_db(sql_query, dictdbName)

    # Iterates in rows and gets the useful parameters from use.
    for column_name, use in rows:
        is_filter[column_name] = use

    return is_filter


# Auxiliary function that returns the tables information.
def _obtainTables():
    # Obtain table_name, column_name, column_key of all columns in DB.
    sqlQuery = "SELECT table_name, column_name, column_key FROM information_schema.columns WHERE table_schema = '{0}' order by table_name".format(
        dbName)

    # Execute the sqlQuery and get answer.
    return _query_db(sqlQuery, dbName)


# Function to obtain a dictionary to convert the values from the database to a user friendly ones.
def _obtainConversionDict():
    conversionDict = {}

    # Obtain table_name, column_name, value_name, UserFriendly_value of all columns in DB.
    sqlQuery = "SELECT type, var_obtained, value, meaning FROM Dictionary"
    rows = _query_db(sqlQuery, dictdbName)
    # Iterates rows in order to convert the values to the user friendly ones.
    for table_name, column_name, value_name, userFriendly_value in rows:
        # Checks if the value is a digit, because SQL saves it as string and adds the "'" character.
        if value_name.strip("'").isdigit():
            conversionDict[(table_name, column_name, int(value_name.strip("'")))] = userFriendly_value
        else:
            conversionDict[(table_name, column_name, value_name)] = userFriendly_value

    return conversionDict


# Function to obtain a dictionary to convert the user friendly values to the ones in the database.
def _obtainInvConversionDict():
    invConversionDict = {}

    # Obtain table_name, column_name, value_name, UserFriendly_value of all columns in DB.
    sqlQuery = "SELECT type, var_obtained, value, meaning FROM Dictionary"
    rows = _query_db(sqlQuery, dictdbName)
    # Iterates rows in order to convert the user friendly values to the ones used in the database.
    for table_name, column_name, value_name, userFriendly_value in rows:
        # Initialize list of values if it has not been done yet.
        if (table_name, column_name, userFriendly_value) not in invConversionDict:
            invConversionDict[(table_name, column_name, userFriendly_value)] = []

        # Checks if the value is a digit, because SQL saves it as string and adds the "'" character.
        if value_name.strip("'").isdigit():
            invConversionDict[(table_name, column_name, userFriendly_value)].append(value_name.strip("'"))
        else:
            invConversionDict[(table_name, column_name, userFriendly_value)].append(value_name)

    return invConversionDict


######## PUBLIC FUNCTIONS ########


# This function returns a dictionary containing all the fields and their corresponding values to search for.
def obtainFilterDict():
    # Obtain table information.
    tableInfo = _obtainTables()

    # Obtain isFilter dictionary.
    isFilter = _obtainIsFilter()

    # Obtain conversion dictionary.
    conversionDict = _obtainConversionDict()

    # Create dictionary to store db info.
    # Tuple of (Table,Column) as key and list of distinct values for the column as value.
    filterDict = {}
    # Iterates table information to build filterDict.
    for table_name, column_name, column_key in tableInfo:
        # Checks if it is a useful filter.
        if isFilter[column_name]:
            # Obtains the values given a column_name and a table_name.
            sqlQuery = "SELECT distinct {0} FROM {1} order by {0}".format(column_name, table_name)
            values = _query_db(sqlQuery, dbName)
            # Initializes the list where the values will be stored.
            filterDict[(table_name, column_name)] = []
            # Iterates through the values to remove the tuple format, becouse SQL returns a tuple of one value tuples. The one value tuple format is "(value,)" .
            for tupled_value in values:
                for value in tupled_value:
                    # Checks wether the value is defined in conversionDict or not. 
                    if (table_name, column_name, value) in conversionDict:
                        # Adds the converted value.
                        filterDict[(table_name, column_name)].append(conversionDict[(table_name, column_name, value)])
                    else:
                        # Adds the value that has no conversion.
                        filterDict[(table_name, column_name)].append(value)
    return filterDict


# This function makes the query to the database by obtaining the dictionary with the fields and corresponding values to search, chosen by the user.
def querySearch(searchDict, urlsFlag=False):
    # Obtain both conversion dictionaries.
    conversionDict = _obtainConversionDict()
    invConversionDict = _obtainInvConversionDict()

    # Initializes the query string.
    sqlQuery = "SELECT idPMT FROM PMT WHERE "

    # Indicates if it is the first iteration to create the query.
    firstFlag = True

    # Iterates through the searchDict to create the query.
    for table_name, column_name in searchDict:
        value = searchDict[(table_name, column_name)]
        # Checks if the value in searchDict is in the invConversionDict to convert to the value used in the database.
        if (table_name, column_name, value) in invConversionDict:
            searchDict[(table_name, column_name)] = invConversionDict[(table_name, column_name, value)]
        # Converts the value into a one-element list to follow the same structure
        else:
            searchDict[(table_name, column_name)] = [value]

        # Checks whether it is the first flag or not, and if it isn't the first, adds an AND to the query string.
        if not firstFlag:
            sqlQuery += " AND "

        # Update firstFlag
        firstFlag = False

        # Indicates if it is the first iteration of elements.
        internalFirstFlag = True

        # Open parenthesis on each filter condition
        sqlQuery += "("

        # Iterate over the list of values
        for element in searchDict[(table_name, column_name)]:

            # Checks whether it is the first flag or not, and if it isn't the first, adds an AND to the query string.
            if not internalFirstFlag:
                sqlQuery += " OR "

            # Update internalFirstFlag
            internalFirstFlag = False

            # Checks whether the value is a digit.
            if element.isdigit():
                value = element
            else:
                # Converts the value into a concrete string format.
                value = "\'{0}\'".format(element)

            # Depending on the table that the column belongs to, a different query needs to be generated. This if elif else, checks all  cases and builds the query.
            if table_name == 'TS':
                sqlQuery += "identifierTS IN (SELECT identifierTS FROM PMT NATURAL JOIN TS WHERE {0}={1})".format(
                    column_name, value)
            elif table_name == 'PMT':
                sqlQuery += "{0}={1}".format(column_name, value)
            elif table_name == 'Stream':
                sqlQuery += "idPMT IN (SELECT idPMT FROM Stream WHERE {0}={1})".format(column_name, value)
            else:
                sqlQuery += "idPMT IN (SELECT idPMT FROM Stream NATURAL JOIN {2} WHERE {0}={1})".format(column_name, value,
                                                                                                        table_name)
        # Close parenthesis after each filter condition
        sqlQuery += ")"


    # Checks if the user wants the URL and adds the necessary query.
    if urlsFlag:
        sqlQuery = "SELECT Path, Service_Name, PIDNumber, URL FROM TS NATURAL JOIN (PMT NATURAL JOIN (Stream NATURAL JOIN (Private NATURAL JOIN URL))) WHERE idPMT IN ({0}) AND HbbTV=1".format(
            sqlQuery)
    else:
        sqlQuery = "SELECT Path, Service_Name, PIDNumber FROM PMT NATURAL JOIN TS WHERE idPMT IN ({0})".format(sqlQuery)

    # Execute the sqlQuery and get answer in rows.
    rows = _query_db(sqlQuery, dbName)

    # Create dictionary to store result info.
    resultDict = {}

    # Dictionary format with urls: resultDict[Path][Service_Name] = [url1,url2,...].
    if urlsFlag:
        for Path, Service_Name, PIDNumber, URL in rows:
            if ('PMT', 'Service_Name', Service_Name) in conversionDict:
                convertedService_Name = conversionDict[('PMT', 'Service_Name', Service_Name)]
            else:
                convertedService_Name = Service_Name
            if convertedService_Name == NOT_DEFINED:
                convertedService_Name = hex(int(PIDNumber))
            if Path not in resultDict:
                resultDict[Path] = {}
            if Service_Name not in resultDict[Path]:
                resultDict[Path][convertedService_Name] = []
            resultDict[Path][convertedService_Name].append(URL)

    # Dictionary format without urls: resultDict[Path] = [Service_Name1,Service_Name2,...].
    else:
        for Path, Service_Name, PIDNumber in rows:
            if ('PMT', 'Service_Name', Service_Name) in conversionDict:
                convertedService_Name = conversionDict[('PMT', 'Service_Name', Service_Name)]
            else:
                convertedService_Name = Service_Name
            if convertedService_Name == NOT_DEFINED:
                convertedService_Name = hex(int(PIDNumber))
            if Path not in resultDict:
                resultDict[Path] = []
            if Service_Name == NOT_DEFINED:
                resultDict[Path].append(convertedService_Name)


    return resultDict
