from pymongo import MongoClient
import configparser

class MongoDB:

	# Creates initial DB connection
	def __init__(self, dbname):
		# reads the config file	
		config = configparser.ConfigParser()
		config.read("config.ini")

		# connects to mongo client
		self.client = MongoClient(config.get("Database", "mongo"))
		self.db = self.client.SampleQueries

	# Creates a new document to be inserted into ProcessedQueries
	# processed is a dictionary object with the proper attributes
	def create_query(self, processed):
		pq = self.db.ProcessedQueries
		query_id = pq.insert_one(processed).inserted_id
		print("Inserted \"" + str(query_id) + "\" for " + str(processed))

	# Find one document in the ProcessedQueries
	# query is the dictionary object with the conditions we are looking for (use {} for any)
	def read_one_query(self, query):
		pq = self.db.ProcessedQueries
		return pq.find_one(query)

	# Find multiple documents in the ProcessedQueries
	# query is the dictionary object with the conditions we are looking for (use {} for any)
	def read_queries(self, query):
		pq = self.db.ProcessedQueries
		return pq.find(query)

	# Get counts of documents matching a query (use {} for all documents)
	def count_queries(self, query):
		pq = self.db.ProcessedQueries
		return pq.count_documents(query)

	# Updates one particular document
	# update should be a dictionary in the form of {{query}, {updates}}
	def update_one_query(self, update):
		pq = self.db.ProcessedQueries
		print(update)
		query_id = pq.find_one_and_update(update[0], {'$set': update[1]})
		print("Query " + str(query_id["_id"]) + " has been updated")

	# Updates many documents
	# update should be a dictionary in the form of {{query}, {updates}}
	def update_queries(self, update):
		pq = self.db.ProcessedQueries
		result = pq.update_many(update[0], {'$set': update[1]})
		print("Updated " + str(result.modified_count) + " documents")

	
	# Deletes one document from ProcessedQueries
	def delete_one_query(self, filter):
		pq = self.db.ProcessedQueries
		result = pq.delete_one(filter)
		print("Deleted " + str(result.deleted_count) + " document")

	# Deletes one document from ProcessedQueries
	def delete_queries(self, filter):
		pq = self.db.ProcessedQueries
		result = pq.delete_many(filter)
		print("Deleted " + str(result.deleted_count) + " document")