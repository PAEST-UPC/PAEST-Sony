import pymysql

def obtainFilterDict():
	# Create a connection object

	dbServerName    = "127.0.0.1"

	dbUser          = "root"

	dbPassword      = "1234"

	dbName          = "world"

	charSet         = "utf8mb4"

	cursorType      = pymysql.cursors.DictCursor


	connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

	                                     db=dbName, charset=charSet)#,cursorclass=cursorType)


	try:

		# Create a cursor object

		cursorObject        = connectionObject.cursor()



	    # SQL query string

		#obtain all column names in table city
		#sqlQuery            = "select column_name from information_schema.columns where table_name = 'city'"

		#obtain all column names in all tables (column,table)
		#sqlQuery            = "select table_name, column_name from information_schema.columns"

		#obtain all column names in city table (column,table)
		sqlQuery            = "select table_name, column_name from information_schema.columns where table_name = 'city'"


		#sqlQuery            = "select * from city

	    # Execute the sqlQuery

		cursorObject.execute(sqlQuery)

		#Fetch all the rows

		rows                = cursorObject.fetchall()

		print(rows)

		filterDict = {}

		for row in rows:
			table_name = row[0]
			column_name = row[1]
			sqlQuery = "select distinct {0} from {1}".format(column_name, table_name)
			cursorObject.execute(sqlQuery)
			options                = cursorObject.fetchall()
			filterDict[column_name] = options 

		return filterDict

	except Exception as e:

		print("Exception occured:{}".format(e))

	finally:

		connectionObject.close()


