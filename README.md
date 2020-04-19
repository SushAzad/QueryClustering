# QueryClustering

## Setup

To set up, please install the following:

`pip3 install configparser`

`pip3 install pymongo`

`pip3 install pymysql`

## Todo 

- [x] Schedule Demo--Sush 
- [x] CRUD scripts--Heather (CR) and Sush (UD) 
- [x] Retrieve keywords--Jiaqi 
- [x] Summarize 04/04 meeting notes--Jiaqi
- [x] Meet with Abdu to finalize criteria--Sush (what would he want queries to be clustered by?)
- [x] Get embeddings for raw data and keywords (Sush)
- [ ] Cluster raw data vs. keywords (Jiaqi)
- [ ] Implement parsing/getting additional features 
- [ ] Create MongoDB to store features (Heather)

#### Advanced 
- [ ] Parsing
	- [ ] Remove alias (Products as P, Products P)
	- [ ] Map all subqueries to the same 
- [ ] Display queries and clusters on front end 

#### Database 
About the Database:
Use the 'pl_queries' database, table name Queries.
Schema:
- queryNum (int): Auto-incremementing primary key. Has no cool info.
- queryID (int): Unique query ID which corresponds to (queryID from) PrairieLearn. In the form of 5 digit random number.
- variantID (int): ID to uniquely identify the question variant. It appears there were multiple variants per question in Fall 2019, so we can treat variantID as a question ID to cluster by.
-queryText (text): Raw untokenized text of the students SQL query.

When tokenizing queryText, make sure to save the tokenized text against the same queryID so we can retrieve the original later.

TO-DO:
- [ ] Foreign key constraints (questionId, cascade/update on delete)

#### Analyzing queries 
- [ ] Distinguish variable names vs. keywords
	* Implement "within quotations"/"within parenthases" 
  * Otherwise, variable names that overlap with keywords will show up in final list
- [ ] Take care of instances like: "Department=" where tokenize does not remove the "=" 
  * Idea: find set of punctuation, and go through and remove common punctuation (will mess with regex?)
  * However, this should only occur with table/variable names. (Need confirmation)
 
