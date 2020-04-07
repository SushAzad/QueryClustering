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
- [ ] Meet with Abdu to finalize criteria--Sush (what would he want queries to be clustered by?)

#### Database 
- [ ] Foreign key constraints (questionId, cascade/update on delete)

#### Analyzing queries 
- [ ] Distinguish variable names vs. keywords
	* Implement "within quotations"/"within parenthases" 
  * Otherwise, variable names that overlap with keywords will show up in final list
- [ ] Take care of instances like: "Department=" where tokenize does not remove the "=" 
  * Idea: find set of punctuation, and go through and remove common punctuation (will mess with regex?)
  * However, this should only occur with table/variable names. (Need confirmation)
  

