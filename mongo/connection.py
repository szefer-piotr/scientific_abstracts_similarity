from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

MONGO_DB_URI = os.environ['MONGO_DB_URI']

# Create a new client and connect to the server
myclient = MongoClient(MONGO_DB_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    myclient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = myclient.abstract_search
collection = db.data