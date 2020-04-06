import crud_operations as co

db = co.MySQLDB("SampleQueries")

# db.create_query(1, 'this is a test insert')
print("Before Insert")
print(db.read_all_questions())

db.create_question("test question insert")

print("After Insert")
print(db.read_all_questions())

print("Testing Update. Before update:")
print(db.read_all_questions())

qid = input("Enter question ID to be updated: ")
q = input("Enter new value for question: ")
db.update_question_by_id(qid, q)
print("After update")
print(db.read_all_questions())

print("Before Delete")
print(db.read_all_questions())
qid = input("Enter question ID to be deleted (Questions Table): ")
db.delete_question_by_id(qid)
print("After Delete")
print(db.read_all_questions())