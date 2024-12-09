import json
from mongo.connection import myclient

mydb = myclient["abstract_search"] #This is my database

print(mydb)

Collection = mydb["data"] # This is my collection

with open('/home/piotr/projects/articles_similarity/scientific_abstracts_similarity/data/arxiv_papers/arxiv-metadata-10000.json', 'r') as file:
    data = json.load(file)

Collection.insert_many(data)