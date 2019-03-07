import pymysql

def createSampleDB():
	# Create a connection object

	dbServerName    = "127.0.0.1"

	dbUser          = "root"

	dbPassword      = "1234"

	charSet         = "utf8mb4"

	cursorType      = pymysql.cursors.DictCursor


	connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

	                                    charset=charSet,cursorclass=cursorType)


	try:

		# Create a cursor object

		cursorObject        = connectionObject.cursor()

		newDB = 'sample'
		sqlQuery = "create database " + newDB

	    
	    # Execute the sqlQuery

		cursorObject.execute(sqlQuery)

		
		sqlQuery = "show databases"
		cursorObject.execute(sqlQuery)
		rows = cursorObject.fetchall()
		for row in rows:
			print(row)

		#Fetch all the rows

		

	except Exception as e:

		print("Exception occured:{}".format(e))

	finally:

		connectionObject.close()

def createSampleTable():
	dbServerName    = "127.0.0.1"

	dbUser          = "root"

	dbPassword      = "1234"

	dbName          = "sample"

	charSet         = "utf8mb4"

	cursorType      = pymysql.cursors.DictCursor


	connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

	                                     db=dbName, charset=charSet,cursorclass=cursorType)


	try:

		# Create a cursor object

		cursorObject        = connectionObject.cursor()

		sqlCreateTableCommand   = "CREATE TABLE EmployeeSample(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)"

		cursorObject.execute(sqlCreateTableCommand)

	except Exception as e:

		print("Exception occured:{}".format(e))

	finally:

		connectionObject.close()



def addSampleTable():
	dbServerName    = "127.0.0.1"

	dbUser          = "root"

	dbPassword      = "1234"

	dbName          = "sample"

	charSet         = "utf8mb4"

	cursorType      = pymysql.cursors.DictCursor


	connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

	                                     db=dbName, charset=charSet,cursorclass=cursorType)


	try:

		# Create a cursor object

		cursorObject        = connectionObject.cursor()

		insertStatement = "INSERT INTO EmployeeSample (id, LastName, FirstName, DepartmentCode) VALUES (7,\"perez\",\"alberto\",11)"
		cursorObject.execute(insertStatement)
		insertStatement = "INSERT INTO EmployeeSample (id, LastName, FirstName, DepartmentCode) VALUES (8,\"martinez\",\"pilar\",10)"
		cursorObject.execute(insertStatement)
		insertStatement = "INSERT INTO EmployeeSample (id, LastName, FirstName, DepartmentCode) VALUES (9,\"martinez\",\"pepa\",9)"
		cursorObject.execute(insertStatement)
		connectionObject.commit()
		sqlQuery    = "select * from employeesample"
		#sqlQuery            = "select table_name, column_name from information_schema.columns where table_name = 'employeesample'"

		cursorObject.execute(sqlQuery)

		rows = cursorObject.fetchall()
		for row in rows:
			print(row)

	except Exception as e:

		print("Exception occured:{}".format(e))

	finally:

		connectionObject.close()

def querySampleTable():
	dbServerName    = "127.0.0.1"

	dbUser          = "root"

	dbPassword      = "1234"

	dbName          = "sample"

	charSet         = "utf8mb4"

	cursorType      = pymysql.cursors.DictCursor


	connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

	                                     db=dbName, charset=charSet,cursorclass=cursorType)


	try:

		# Create a cursor object

		cursorObject        = connectionObject.cursor()

		sqlQuery = "select * from employeesample"
		cursorObject.execute(sqlQuery)

		rows = cursorObject.fetchall()
		for row in rows:
			print(row)

	except Exception as e:

		print("Exception occured:{}".format(e))

	finally:

		connectionObject.close()



querySampleTable()

