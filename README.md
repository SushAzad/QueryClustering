# QueryClustering

## Setup

To set up, please install the following:

`pip3 install configparser`

`pip3 install pymongo`

`pip3 install pymysql`



## Database 
About the Database:
Use the 'pl_queries' database, table name Queries.
Schema:
- queryNum (int): Auto-incremementing primary key. Has no cool info.
- queryID (int): Query ID which corresponds to (queryID from) PrairieLearn. In the form of 5 digit random number. Only have 212 of these for 1418 unique queries, so this might be a student ID???
- variantID (int): ID to uniquely identify the question variant. It appears there were multiple variants per question in Fall 2019, so we can treat variantID as a question ID to cluster by.
- queryText (text): Raw untokenized text of the students SQL query.

When tokenizing queryText, make sure to save the tokenized text against the same queryID so we can retrieve the original later.


## Getting Embeddings:

The file call the file `createEmbeddings.py` in the following way:

python createEmbeddings.py [path+filename] [boolean]

- The file should consist of a csv file with 2 columns - queryID (corresponding to pl_queries.Queries) & queryText. If you want to use the raw queries, we can pass in './data/fa19_queries.csv', which has all the records from fa19 pulled from the Queries table. These queries are not tokenized already, so pass 'False' for the boolean, and it will nltk tokenize it ebfore creating embeddings.
	- Eg usage: python createEmbeddings.py ./data/fa19_queries.csv False

- If the queries have been tokenized in some other way, store those queries in a csv file, with the queryID column corresponding  to the queryID of the record in the database. pass 'True' for the boolean in this case, so no further tokenization is done.
	- Eg usage: python createEmbeddings.py ./data/your_file.csv True
	
The embeddings will be stored in a pickle file called 'NewQueryEmbeddings'. When read into a dictionary, the keys will be the QueryIDs from the given csv file, and its value will be the document embeddings generated for that query.




## Todo 

- [x] Schedule Demo--Sush 
- [x] CRUD scripts--Heather (CR) and Sush (UD) 
- [x] Retrieve keywords--Jiaqi 
- [x] Summarize 04/04 meeting notes--Jiaqi
- [x] Meet with Abdu to finalize criteria--Sush (what would he want queries to be clustered by?)
- [x] Get embeddings for raw data and keywords (Sush)
- [ ] Cluster raw data vs. keywords (Jiaqi)
- [ ] Implement parsing (Heather)
- [ ] Get additional features 
- [x] Create MongoDB to store features (Heather)

#### Advanced 
- [ ] Parsing
	- [ ] Remove alias (Products as P, Products P)
	- [ ] Map all subqueries to the same 
- [ ] Display queries and clusters on front end 


TO-DO:
- [ ] Foreign key constraints (questionId, cascade/update on delete)


#### Analyzing queries 
- [ ] Distinguish variable names vs. keywords
	* Implement "within quotations"/"within parenthases" 
  * Otherwise, variable names that overlap with keywords will show up in final list
- [ ] Take care of instances like: "Department=" where tokenize does not remove the "=" 
  * Idea: find set of punctuation, and go through and remove common punctuation (will mess with regex?)
  * However, this should only occur with table/variable names. (Need confirmation)
 
