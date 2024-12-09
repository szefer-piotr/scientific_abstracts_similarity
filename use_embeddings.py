from mongo.connection import collection
from utils.functions import generate_embedding

query = "Markov Monte Carlo"

results = collection.aggregate([
    {"$vectorSearch": {
        "queryVector": generate_embedding(query),
        "path": "abstract_embedding_hf",
        "numCandidates": 100,
        "limit": 4,
        "index": "vector_index",
    }}
])

for document in results:
    print(f"Paper Title: {document['title']},\nAbstract: {document['abstract']}\n")