from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
mongodb_uri = os.getenv('MONGO_DB_URI')

class MongoConnector:
    def __init__(self, database_name: str, collection_name: str):
        self.client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def close(self):
        self.client.close()



# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# import os
# from dotenv import load_dotenv

# load_dotenv()
# MONGO_DB_URI = os.getenv('MONGO_DB_URI')

# # Create a new client and connect to the server
# myclient = MongoClient(MONGO_DB_URI, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     myclient.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# db = myclient.abstract_search
# collection = db.data