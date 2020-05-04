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

	# Creates a new query record
	def create_query(self, question, query):
		sql = "INSERT INTO `hw1` (`questionid`, `query`) VALUES (%s, %s)"
		self.mycursor.execute(sql, (question, query))
		self.conn.commit()
		print("Inserted \"" + query + "\" for question " + str(question))

	def create_query_Queries(self, queryID, vID, qText):
		sql = "INSERT INTO `Queries` (`queryID`, `VariantID`, `QueryText`) VALUES (%s, %s, %s)"
		self.mycursor.execute(sql, (queryID, vID, qText))
		self.conn.commit()
		print("Inserted \"" + queryID + "\" for question " + str(vID))

	def create_question(self, content):
		sql = "INSERT INTO `Questions` (`question`) VALUES (%s)"
		self.mycursor.execute(sql, (content))
		self.conn.commit()
		print("Inserted the question:", content)
	

	# returns queryid, questionid, queryContent
	def read_queries_for_question(self, questionid):
		sql = "SELECT * FROM `hw1` WHERE `questionid`=%s"
		self.mycursor.execute(sql, (questionid))
		result = self.mycursor.fetchall()
		return result

	# returns questionid, questionContent
	def read_question(self, questionid):
		sql = "SELECT * FROM `Questions` WHERE `questionid`=%s"
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
	def readAllQueries(self):
		sql = "SELECT * FROM `Queries`"
		self.mycursor.execute(sql)
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
		sql = "UPDATE `hw1` SET `query`=%s WHERE `queryid`=%s"
		self.mycursor.execute(sql, (query, queryid))
		result = self.mycursor.fetchall()
		return result

	# updates all the queries for one question
	def update_all_queries(self, questionid, query):
		sql = "UPDATE `hw1` SET `query`=%s WHERE `questionid`=%s"
		self.mycursor.execute(sql, (query, questionid))
		self.conn.commit()
		print("Updated hw1 for questionID= ", questionid)
		return()

	# updates a particular question by id
	def update_question_by_id(self, questionid, question):
		sql = "UPDATE `Questions` SET `question`=%s WHERE `questionid`=%s"
		self.mycursor.execute(sql, (question, questionid))
		self.conn.commit()
		print("Updated Questions for questionID= ", questionid)
		return

	# deletes a particular question by id
	def delete_question_by_id(self, questionid):
		sql = "DELETE FROM `Questions` WHERE `questionid`=%s"
		self.mycursor.execute(sql, (questionid))
		self.conn.commit()
		print("Deleted from Questions for questionID= ", questionid)
		return 

	# deletes a particular query by id
	def delete_query_by_id(self, queryid):
		sql = "DELETE FROM `hw1` WHERE `queryid`=%s"
		self.mycursor.execute(sql, (queryid))
		self.conn.commit()
		print("Deleted from hw1 for queryid= ", queryid)
		return

	# deletes all queries for one questionid (i.e. if we delete a question for example)
	def delete_all_queries(self, questionid):
		sql = "DELETE FROM `hw1` WHERE `questionid`=%s"
		self.mycursor.execute(sql, (questionid))
		self.conn.commit()
		print("Deleted All queries in hw1 for questionID= ", questionid)
		return


