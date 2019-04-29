import pymysql


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
    connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,
                                         db=dbName, charset=charSet)#,cursorclass=cursorType)
    try:
        # Create a cursor object
        cursorObject = connectionObject.cursor()

        # Execute the sqlQuery
        #print('Quering DB: ' + sqlQuery)
        cursorObject.execute(sqlQuery)

        # Fetch all the rows
        return cursorObject.fetchall()
    
    except Exception as e:

        print("Exception occured:{}".format(e))

    finally:

        connectionObject.close()


# Auxiliary function that returns
def _obtainPKInfo():

    # Obtain table_name, column_name, column_key of all columns in DB
    sqlQuery = "SELECT table_name, column_name, column_key FROM information_schema.columns WHERE table_schema = '{0}' order by table_name".format(dbName)

    # Execute the sqlQuery and get answer
    return _queryDB(sqlQuery,dbName)

######## PUBLIC FUNCTIONS ########

# This function returns a dictionary containing all the needed info to start the GUI
def obtainFilterDict():

    # Obtain PKInfo()
    PKInfo = _obtainPKInfo()

    # Create dictionary to store db info
    # Tuple of (Table,Column) as key and list of distinct values for the column as value
    filterDict = {}
    for table_name, column_name, column_key in PKInfo:
        sqlQuery = "SELECT distinct {0} FROM {1} order by {0}".format(column_name, table_name)
        filterDict[(table_name,column_name)] = _queryDB(sqlQuery,dbName) 
    
    return filterDict

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
def obtainFilterDictMT():
    
    # Obtain PKInfo()
    PKInfo = _obtainPKInfo()

    # Create dictionary to store db info
    # Tuple of (Table,Column) as key and list of distinct values for the column as value
    filterDict = {}
    for table_name, column_name, column_key in PKInfo:
        if not column_key:
            sqlQuery = "SELECT distinct {0} FROM {1} order by {0}".format(column_name, table_name)
            filterDict[(table_name,column_name)] = _queryDB(sqlQuery,dbName)
    del filterDict[('URL','URL')]
    return filterDict


def querySearch(searchDict):

    sqlQuery = ""

    firstFlag = True
    for table_name, column_name in searchDict:

        if searchDict[(table_name,column_name)].isdigit():
            value = searchDict[(table_name,column_name)]
        else:
            value = "\'{0}\'".format(searchDict[(table_name,column_name)])

        if firstFlag:
            sqlQuery += "SELECT * FROM {0} WHERE {1}={2}".format(table_name,column_name,value)
            firstFlag = False
        else:
            sqlQuery += " and {0}={1}".format(column_name,value)

    
     # Execute the sqlQuery and get answer in rows
    rows = _queryDB(sqlQuery,dbName)

    return rows

def querySearchMT(searchDict, urlsFlag=False):
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

    sqlQuery = "SELECT Path, Service_Name FROM PMT NATURAL JOIN TS WHERE idPMT IN ({0})".format(sqlQuery)
    
    if urlsFlag:
        sqlQuery = "SELECT Path, Service_Name, URL FROM PMT NATURAL JOIN (Stream NATURAL JOIN (Private NATURAL JOIN URL)) WHERE idPMT IN ({0}) AND HBBT=1".format(sqlQuery)


    # Execute the sqlQuery and get answer in rows
    rows = _queryDB(sqlQuery,dbName)
    
    # Create dictionary to store result info
    resultDict = {}

    # Dictionary format with urls: resultDict[identifierTS][Service_Name] = [url1,url2,...]
    if urlsFlag:
        for Path, Service_Name, URL in rows:
            if Path not in resultDict:
                resultDict[Path] = {}
            if hex(Service_Name).upper() not in resultDict[Path]:
                resultDict[Path][hex(Service_Name).upper()] = []
            resultDict[Path][hex(Service_Name).upper()].append(URL)
    
    # Dictionary format without urls: resultDict[Path] = [Service_Name1,Service_Name2,...]
    else:
        for Path, Service_Name in rows:
            if Path not in resultDict:
                resultDict[Path] = []
            resultDict[Path].append(hex(Service_Name).upper())
    return resultDict

if __name__ == "__main__":
    print(obtainConversionDict())
    #print(obtainFilterDictMT())
    