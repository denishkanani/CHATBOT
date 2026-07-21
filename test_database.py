from database import Database

db = Database()

db.add_document(
    "101",
    "Machine Learning",
    "Wikipedia"
)

db.save_search(
    "What is Machine Learning?",
    "Machine Learning is a subset of AI."
)

print("Documents:")
print(db.get_documents())

print("\nHistory:")
print(db.get_search_history())

db.close()