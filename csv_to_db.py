import csv
import crud_operations as co
import sys

def qPrint(query):
    print(query[0] + "\t" + query[2] + "\t" + query[1])

def getQueries(filename):
	queries = []
	qCounter = 0
	with open(filename) as tsv:
	    reader = csv.reader(tsv, delimiter=',')
	    for idx, row in enumerate(reader):
	        if idx != 0:
	            # queryID, variantID, queryText
	            entry = []
	            entry.append(row[0])
	            entry.append(row[1])
	            entry.append(row[2])
	            entry.append(str(qCounter))
	            qCounter += 1
	            queries.append(entry)

	print("quesId\tqueryId\tQueryContent")
	for i in range(0,5):
	    qPrint(queries[i])
	return queries

# Get the queries from CSV
if (len(sys.argv) < 2):
	print("Please input a file to use i.e. python csv_to_db.py [file]")
else:
	filename = sys.argv[1]
	# we currently have sql_queries.tsv
	toInsert = getQueries(filename)

	# Create db object for querying (insert into SampleQueries db)
	db = co.MySQLDB("pl_queries")

	# Insert all entries in toInsert
	for entry in toInsert:
		db.create_query_Queries(entry[0], entry[1], entry[2])

	print("Inserted queries into db")

