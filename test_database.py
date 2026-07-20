from src.database import get_collection, populate_database

populate_database()

collection = get_collection()

print("\nCollection Name:", collection.name)
print("Documents:", collection.count())