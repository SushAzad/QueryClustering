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
	def read_all_queries(self):
		sql = "SELECT * FROM `hw1`"
		self.mycursor.execute(sql)
		result = self.mycursor.fetchall()
		return result

	# updates a particular query by id
	def update_query_by_id(self, queryid):
		pass

	# updates all the queries for one question
	def update_all_queries(self, questionid):
		pass

	# updates a particular question by id
	def update_question_by_id(self, questionid):
		pass

	# deletes a particular question by id
	def delete_question_by_id(self, questionid):
		pass

	# deletes a particular query by id
	def delete_query_by_id(self, queryid):
		pass

	# deletes all queries for one questionid (i.e. if we delete a question for example)
	def delete_all_queries(self, questionid):
		pass

