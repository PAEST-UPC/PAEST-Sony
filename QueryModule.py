import pymysql


# DB server variables
dbServerName = "127.0.0.1"
dbUser = "ubuntu"
dbPassword = "paesa19"
dbName = "searcherTest"
charSet = "utf8mb4"
#cursorType = pymysql.cursors.DictCursor

######## PRIVATE FUNCTIONS ########

# Auxiliary private function that encapsulates queries to the DB
def _queryDB(sqlQuery):
	# Create a connection object
	connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,
	                                     db=dbName, charset=charSet)#,cursorclass=cursorType)
	try:
		# Create a cursor object
		cursorObject = connectionObject.cursor()

		# Execute the sqlQuery
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
	sqlQuery = f"select table_name, column_name, column_key from information_schema.columns where table_schema = '{dbName}' order by table_name"

    # Execute the sqlQuery and get answer
	return _queryDB(sqlQuery)

######## PUBLIC FUNCTIONS ########

# This function returns a dictionary containing all the needed info to start the GUI
def obtainFilterDict():

    # Obtain PKInfo()
	PKInfo = _obtainPKInfo()

	# Create dictionary to store db info
	# Tuple of (Table,Column) as key and list of distinct values for the column as value
	filterDict = {}
	for table_name, column_name, column_key in PKInfo:
		sqlQuery = "select distinct {0} from {1} order by {0}".format(column_name, table_name)
		filterDict[(table_name,column_name)] = _queryDB(sqlQuery) 
	
	return filterDict


# This function returns a dictionary containing all the needed info to start the GUI from MultiTable DB
def obtainFilterDictMT():
	
    # Obtain PKInfo()
	PKInfo = _obtainPKInfo()

	# Create dictionary to store db info
	# Tuple of (Table,Column) as key and list of distinct values for the column as value
	filterDict = {}
	for table_name, column_name, column_key in PKInfo:
		if not column_key:
			sqlQuery = "select distinct {0} from {1} order by {0}".format(column_name, table_name)
			filterDict[(table_name,column_name)] = _queryDB(sqlQuery)
	
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
			sqlQuery += "select * from {0} where {1}={2}".format(table_name,column_name,value)
			firstFlag = False
		else:
			sqlQuery += " and {0}={1}".format(column_name,value)

	
	 # Execute the sqlQuery and get answer in rows
	print('Quering DB: ' + sqlQuery)
	rows = _queryDB(sqlQuery)

	return rows

def querySearchMT(searchDict):

	# Obtain PKInfo()
	PKInfo = _obtainPKInfo()

	sqlQuery = ""

	firstFlag = True
	for table_name, column_name in searchDict:

		if searchDict[(table_name,column_name)].isdigit():
			value = searchDict[(table_name,column_name)]
		else:
			value = "\'{0}\'".format(searchDict[(table_name,column_name)])

		if firstFlag:
			sqlQuery += "select * from {0} where {1}={2}".format(table_name,column_name,value)
			firstFlag = False
		else:
			sqlQuery += " and {0}={1}".format(column_name,value)

	
	 # Execute the sqlQuery and get answer in rows
	print('Quering DB: ' + sqlQuery)
	rows = _queryDB(sqlQuery)

	return rows


print(obtainFilterDictMT())