from src.databases.mongo.connection import collection
from src.utils.generate_embeddings import generate_embedding

# Upload embeddings to the MongoDB database
for doc in collection.find({'abstract':{"$exists": True}}).limit(50):
    doc['abstract_embedding_hf'] = generate_embedding(doc['abstract'])
    collection.replace_one({'_id': doc['_id']}, doc)