import pymysql


# This function returns a dictionary containing all the needed info to start the GUI
def obtainFilterDict():
	# Create a connection object
	dbServerName = "127.0.0.1"
	dbUser = "root"
	dbPassword = "1234"
	dbName = "sample"
	charSet = "utf8mb4"
	#cursorType = pymysql.cursors.DictCursor

	connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

	                                     db=dbName, charset=charSet)#,cursorclass=cursorType)

	try:
		# Create a cursor object
		cursorObject        = connectionObject.cursor()

	    # SQL query string
		# Obtain all column names in employeesample table in format (table,name)
		sqlQuery = "select table_name, column_name from information_schema.columns where table_name = 'employeesample'"

	    # Execute the sqlQuery
		cursorObject.execute(sqlQuery)

		# Fetch all the rows
		rows = cursorObject.fetchall()

		# Create dictionary to store db info
		# Columns as keys and list of distinct values for the column as value
		filterDict = {}
		for row in rows:
			table_name = row[0]
			column_name = row[1]
			sqlQuery = "select distinct {0} from {1} order by {0}".format(column_name, table_name)
			cursorObject.execute(sqlQuery)
			options                = cursorObject.fetchall()
			filterDict[column_name] = options 
		
		return filterDict

	except Exception as e:

		print("Exception occured:{}".format(e))

	finally:

		connectionObject.close()
