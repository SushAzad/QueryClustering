import crud_operations as co

db = co.MySQLDB()

# db.create_query(1, 'this is a test insert')
print("Before Insert")
print(db.read_all_questions())

db.create_question("test question insert")

print("After Insert")
print(db.read_all_questions())