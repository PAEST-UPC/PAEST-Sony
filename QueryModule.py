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
    sqlQuery = f"SELECT table_name, column_name, column_key FROM information_schema.columns WHERE table_schema = '{dbName}' order by table_name"

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
    sqlQuery = f"SELECT type, var_obtained, value, meaning FROM Dictionary"
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
    sqlQuery = f"SELECT type, var_obtained, value, meaning FROM Dictionary"
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
        return 'SELECT something'
    else:
        if urlsFlag:
            sqlQuery = "SELECT idPMT FROM PMT WHERE "
        else:
            sqlQuery = "SELECT identifierTS, PIDNumber FROM PMT WHERE "

        firstFlag = True
        for table_name, column_name in searchDict:
            if not firstFlag:
                sqlQuery += " AND "
            
            if searchDict[(table_name,column_name)].isdigit():
                value = searchDict[(table_name,column_name)]
            else:
                value = "\'{0}\'".format(searchDict[(table_name,column_name)])

            if table_name == 'TS':
                sqlQuery += f"identifierTS IN (SELECT identifierTS FROM PMT NATURAL JOIN TS WHERE {column_name}={value})"
            elif table_name == 'PMT':
                sqlQuery += f"{column_name}={value}"
            elif table_name == 'Stream':
                sqlQuery += f"idPMT IN (SELECT idPMT FROM Stream WHERE {column_name}={value})"
            else:
                sqlQuery += f"idPMT IN (SELECT idPMT FROM Stream NATURAL JOIN {table_name} WHERE {column_name}={value})"
            firstFlag = False

    if urlsFlag:
        sqlQuery = f"SELECT identifierTS, PIDNumber, URL FROM PMT NATURAL JOIN (Stream NATURAL JOIN (Private NATURAL JOIN URL)) WHERE idPMT IN ({sqlQuery}) AND HBBT=1"


    # Execute the sqlQuery and get answer in rows
    rows = _queryDB(sqlQuery,dbName)
    
    # Create dictionary to store result info
    resultDict = {}

    # Dictionary format with urls: resultDict[identifierTS][PIDNumber] = [url1,url2,...]
    if urlsFlag:
        for identifierTS, PIDNumber, URL in rows:
            if identifierTS not in resultDict:
                resultDict[identifierTS] = {}
            if hex(PIDNumber).upper() not in resultDict[identifierTS]:
                resultDict[identifierTS][hex(PIDNumber).upper()] = []
            resultDict[identifierTS][hex(PIDNumber).upper()].append(URL)
    
    # Dictionary format without urls: resultDict[identifierTS] = [PIDNumber1,PIDNumber2,...]
    else:
        for identifierTS, PIDNumber in rows:
            if identifierTS not in resultDict:
                resultDict[identifierTS] = []
            resultDict[identifierTS].append(hex(PIDNumber).upper())
    return resultDict

if __name__ == "__main__":
    #print(obtainConversionDict())
    print(obtainFilterDictMT())
    