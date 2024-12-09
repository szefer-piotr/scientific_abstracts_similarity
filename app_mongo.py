from mongo.connection import myclient

import requests
import os

API_URL = os.environ['API_URL']
HF_TOKEN = os.environ['HF_TOKEN']

db = myclient.abstract_search
collection = db.data

# Create embeddings using HuggingFace all_miniLM-l6-v2
def generate_embedding(text: str) -> list[float]:

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": text}
    )

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")
    
    return response.json()

for doc in collection.find({'abstract':{"$exists": True}}).limit(50):
    doc['abstract_embedding_hf'] = generate_embedding(doc['abstract'])
    collection.replace_one({'_id': doc['_id']}, doc)
