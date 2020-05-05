import pymysql
import configparser

class MySQLDB:

	# Creates initial DB connection
	def __init__(self, dbname):
		# reads the config file	
		config = configparser.ConfigParser()
		config.read("config.ini")

		self.conn = pymysql.connect(
			host = config.get("Database", "mysql_ip"),
			user = config.get("Database", "mysql_user"),
			passwd = config.get("Database", "mysql_pw"))

		self.mycursor = self.conn.cursor()
		# currently using `SampleQueries` database; can change if we make new one
		sql = "USE %s" % dbname
		self.mycursor.execute(sql)


	# create table for storing pl_queries questions
	def create_questions_table(self):
		sql="CREATE TABLE pl_queries.Questions ( variantID INT PRIMARY KEY, title VARCHAR (250) NOT NULL);" 
		self.mycursor.execute(sql)
		self.conn.commit()
		print("Created")

	# Creates a new query record
	# def create_query(self, question, query):
	# 	sql = "INSERT INTO `hw1` (`questionid`, `query`) VALUES (%s, %s)"
	# 	self.mycursor.execute(sql, (question, query))
	# 	self.conn.commit()
	# 	print("Inserted \"" + query + "\" for question " + str(question))

	def create_query(self, queryID, vID, qText):
		sql = "INSERT INTO `Queries` (`queryID`, `VariantID`, `QueryText`) VALUES (%s, %s, %s)"
		self.mycursor.execute(sql, (queryID, vID, qText))
		self.conn.commit()
		print("Inserted \"" + str(queryID) + "\" for question " + str(vID))

	# def create_question(self, content):
	# 	sql = "INSERT INTO `Questions` (`question`) VALUES (%s)"
	# 	self.mycursor.execute(sql, (content))
	# 	self.conn.commit()
	# 	print("Inserted the question:", content)

	def create_question(self, variantID, content):
		sql = "INSERT INTO `Questions` (`variantID`, `title`) VALUES (%s, %s)"
		self.mycursor.execute(sql, (variantID, content))
		self.conn.commit()
		print("Inserted the question:", content)
	
	def free_query(self, sql):
		print(sql)
		self.mycursor.execute(sql)
		result = self.mycursor.fetchall()

		
		print("SQL executed")
		return result 

	# returns queryid, questionid, queryContent
	def read_queries_for_question(self, questionid):
		sql = "SELECT * FROM `Queries` WHERE `variantID`=%s"
		self.mycursor.execute(sql, (questionid))
		result = self.mycursor.fetchall()
		return result

	# returns questionid, questionContent
	def read_question(self, questionid):
		sql = "SELECT * FROM `Questions` WHERE `variantID`=%s"
		self.mycursor.execute(sql, (questionid))
		result = self.mycursor.fetchall()
		return result

	# returns all questions
	def read_all_questions(self):
		sql = "SELECT * FROM `Questions`"
		self.mycursor.execute(sql)
		result = self.mycursor.fetchall()
		return result

	# returns all queries
	def read_all_queries(self):
		sql = "SELECT * FROM `Queries`"
		self.mycursor.execute(sql)
		result = self.mycursor.fetchall()
		return result


	def read_query(self, queryNum): 
		sql = "SELECT * FROM `Queries` WHERE `queryNum`=%s"
		self.mycursor.execute(sql, (queryNum))
		result = self.mycursor.fetchall()
		return result

	# added for new PL queries table 
	def get_question_ids(self):
		sql="SELECT variantID FROM `Queries` GROUP BY variantID"
		self.mycursor.execute(sql)
		result = self.mycursor.fetchall()
		return result

	# updates a particular query by id
	def update_query_by_id(self, queryid, query):
		sql = "UPDATE `Queries` SET `queryText`=%s WHERE `queryNum`=%s"
		self.mycursor.execute(sql, (query, queryid))
		result = self.mycursor.fetchall()
		return result

	# updates all the queries for one question
	def update_all_queries(self, questionid, query):
		sql = "UPDATE `Queries` SET `query`=%s WHERE `variantID`=%s"
		self.mycursor.execute(sql, (query, questionid))
		self.conn.commit()
		print("Updated Queries for variantID= ", questionid)
		return()

	# updates a particular question by id
	def update_question_by_id(self, questionid, question):
		sql = "UPDATE `Questions` SET `title`=%s WHERE `variantID`=%s"
		self.mycursor.execute(sql, (question, questionid))
		self.conn.commit()
		print("Updated Questions for variantID= ", questionid)
		return

	# deletes a particular question by id
	def delete_question_by_id(self, questionid):
		sql = "DELETE FROM `Questions` WHERE `variantID`=%s"
		self.mycursor.execute(sql, (questionid))
		self.conn.commit()
		print("Deleted from Questions for variantID= ", questionid)
		return 

	# deletes a particular query by id
	def delete_query_by_id(self, queryNum):
		sql = "DELETE FROM `Queries` WHERE `queryNum`=%s"
		self.mycursor.execute(sql, (queryNum))
		self.conn.commit()
		print("Deleted from Queries for queryNum= ", queryNum)
		return

	# deletes all queries for one questionid (i.e. if we delete a question for example)
	def delete_all_queries(self, questionid):
		sql = "DELETE FROM `Queries` WHERE `variantID`=%s"
		self.mycursor.execute(sql, (questionid))
		self.conn.commit()
		print("Deleted All queries in Queries for variantID= ", questionid)
		return


