from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Select database and collection
# it will be created if not exist !!
db = client['mydatabase']
collection = db['mycollection']

# --- CREATE ---
# Insert multiple documents for demonstration
documents = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Alice", "age": 25, "city": "Los Angeles"},
]
inserted_ids = collection.insert_many(documents).inserted_ids
print(f"Inserted document IDs: {inserted_ids}")

# --- READ ---
# Fetch all documents
print("\nAll documents in collection:")
for doc in collection.find():
    print(doc)

# Find a specific document
print("\nFind one document where name is 'Alice':")
print(collection.find_one({"name": "Alice"}))

# --- UPDATE ---
# 1. Basic update: update one document
update_result = collection.update_one(
    {"name": "Alice"},
    {"$set": {"age": 28}}
)

# 2. Update multiple documents with multiple conditions (AND)
filter_conditions = {
    "name": "Alice",
    "city": "Los Angeles"
}
update_result = collection.update_many(
    filter_conditions,
    {"$set": {"age": 26}}
)
# 3. Update with OR condition using $or
or_condition = {
    "$or": [
        {"name": "Bob"},
        {"city": "Chicago"}
    ]
}
update_result = collection.update_many(
    or_condition,
    {"$inc": {"age": 1}}  # Increment age by 1
)

query = {
    "$or": [
        {
            "$and": [
                {"field1": 1},
                {"field2": 2}
            ]
        },
        {"field3": 3}
    ]
}
results = collection.find(query)
for doc in results:
    print(doc)

# --- DELETE ---
# Delete one document
delete_result = collection.delete_one({"name": "Charlie"})
print(f"\nDeleted {delete_result.deleted_count} document(s) with name 'Charlie'.")

# Delete multiple documents with a condition
delete_many_result = collection.delete_many({"age": {"$gte": 30}})
print(f"Deleted {delete_many_result.deleted_count} documents with age >= 30.")

# --- READ After Deletions ---
print("\nRemaining documents after deletions:")
for doc in collection.find():
    print(doc)


from pymongo import MongoClient

# Connect to MongoDB (Make sure MongoDB is running locally)
client = MongoClient('mongodb://localhost:27017/')

# Access a database and collection
db = client['mydatabase']
collection = db['mycollection']

# Example documents to insert (for illustration purposes)
# Uncomment the following lines to insert sample data if needed

# sample_docs = [
#     {
#         "name": "Document 1",
#         "tags": ["mongodb", "database", "python"],
#         "address": {
#             "city": "New York",
#             "zip": "10001"
#         }
#     },
#     {
#         "name": "Document 2",
#         "tags": ["sql", "database"],
#         "address": {
#             "city": "Los Angeles",
#             "zip": "90001"
#         }
#     }
# ]
# collection.insert_many(sample_docs)

# 1. Find documents where 'tags' contains a specific value ("mongodb")
query_tags_contains_value = {"tags": "mongodb"}

# 2. Find documents where 'tags' contains all specified values
query_tags_all = {"tags": {"$all": ["python", "database"]}}

# 3. Find documents where 'tags' contains any of the specified values
query_tags_in = {"tags": {"$in": ["mongodb", "sql"]}}

# 4. Find documents where 'address.city' is "New York" (nested field)
query_nested_field = {"address.city": "New York"}

# 5. Find documents where 'address' contains both 'city' and 'zip' with specific values
query_nested_multiple_fields = {
    "address": {
        "$elemMatch": {
            "city": "New York",
            "zip": "10001"
        }
    }
}

# Note: The above "$elemMatch" is used when 'address' is an array of sub-documents.
# For a single sub-document, just match with dot notation:
query_single_address = {"address.city": "New York", "address.zip": "10001"}

# Execute the queries and print results
print("Documents where 'tags' contains 'mongodb':")
for doc in collection.find(query_tags_contains_value):
    print(doc)

print("\nDocuments where 'tags' contain all ['python', 'database']:")
for doc in collection.find(query_tags_all):
    print(doc)

print("\nDocuments where 'tags' contain any of ['mongodb', 'sql']:")
for doc in collection.find(query_tags_in):
    print(doc)

print("\nDocuments where 'address.city' is 'New York':")
for doc in collection.find(query_nested_field):
    print(doc)

print("\nDocuments where 'address' contains both 'city'='New York' and 'zip'='10001':")
for doc in collection.find(query_single_address):
    print(doc)
"""
nested of nested 
"""

# Sample documents with nested inside nested structures
sample_docs = [
    {
        "name": "Alice",
        "contact": {
            "address": {
                "city": "New York",
                "zip": "10001"
            },
            "phone": {
                "mobile": "111-222-3333",
                "home": "444-555-6666"
            }
        }
    },
    {
        "name": "Bob",
        "contact": {
            "address": {
                "city": "Los Angeles",
                "zip": "90001"
            },
            "phone": {
                "mobile": "777-888-9999",
                "home": "000-111-2222"
            }
        }
    },
    # Document with array of contacts
    {
        "name": "Charlie",
        "contacts": [
            {
                "address": {
                    "city": "Chicago",
                    "zip": "60601"
                },
                "phone": {
                    "mobile": "123-456-7890",
                    "home": "098-765-4321"
                }
            },
            {
                "address": {
                    "city": "Houston",
                    "zip": "77001"
                },
                "phone": {
                    "mobile": "555-555-5555",
                    "home": "666-666-6666"
                }
            }
        ]
    }
]

# Insert sample data
collection.insert_many(sample_docs)

# 1. Query documents where nested field 'contact.address.city' == "New York"
print("Documents where contact.address.city is 'New York':")
for doc in collection.find({"contact.address.city": "New York"}):
    print(doc)

# 2. Query documents where nested fields 'contact.address.city' == "Los Angeles" AND 'contact.phone.home' == "000-111-2222"
print("\nDocuments where contact.address.city is 'Los Angeles' AND contact.phone.home is '000-111-2222':")
for doc in collection.find({
    "contact.address.city": "Los Angeles",
    "contact.phone.home": "000-111-2222"
}):
    print(doc)

# 3. Query documents where in an array 'contacts', at least one contact has 'address.city' == "Houston"
print("\nDocuments with a contact in Houston inside 'contacts' array:")
for doc in collection.find({
    "contacts": {
        "$elemMatch": {
            "address.city": "Houston"
        }
    }
}):
    print(doc)

# 4. Query documents where nested 'contact.address' has 'city' == "Chicago" and 'zip' == "60601"
print("\nDocuments where contact.address.city is 'Chicago' and zip is '60601':")
for doc in collection.find({
    "contact.address.city": "Chicago",
    "contact.address.zip": "60601"
}):
    print(doc)

# 5. Query documents where 'contacts' array has a contact with 'city' == "Houston" and 'home' phone == "666-666-6666"
print("\nContacts array contains Houston with home phone 666-666-6666:")
for doc in collection.find({
    "contacts": {
        "$elemMatch": {
            "address.city": "Houston",
            "phone.home": "666-666-6666"
        }
    }
}):
    print(doc)
collection.update_one({"_id": ObjectId(post_id)}, {"$set": post_dict})
# Close the connection
client.close()