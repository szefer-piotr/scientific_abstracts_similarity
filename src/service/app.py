from src.utils.functions import generate_embedding
import logging

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import uvicorn

from src.service.schemas.requests import SearchRequest
from src.service.schemas.responses import SearchResponse

from src.databases.redis.connection.connector import RedisConnector
from src.databases.redis.clients.search import SearchRedisClient

from src.databases.postgres.connection.connector import PostgresConnector
from src.databases.postgres.clients.search import SearchPostgresClient

from src.databases.mongo.connection.connector import MongoConnector

app = FastAPI()

redis_connector = RedisConnector()
search_redis_client = SearchRedisClient(connector=redis_connector)

postgres_connector = PostgresConnector()
search_postgres_client = SearchPostgresClient(connector=postgres_connector)

mongo_connector = MongoConnector(
    database_name="abstract_search", 
    collection_name="data")

@app.post("/similar_abstracts")
def find_similar_abstracts(
    request: SearchRequest
    ) -> SearchResponse:
    
    logging.info(f"Received request: {request=}")

    # breakpoint()
 
    cached_response = search_redis_client.read(request)

    query = request.model_dump()['query']
    
    if cached_response is not None:
        print("Cache hit!")
        search_postgres_client.write(
            request=request, 
            response=SearchResponse(items=cached_response.items)
        )
        return cached_response
    
    print("Cache miss!")
    
    # breakpoint()
    
    results = mongo_connector.collection.aggregate([
        {"$vectorSearch": {
            "queryVector": generate_embedding(query),
            "path": "abstract_embedding_hf",
            "numCandidates": 100,
            "limit": 4,
            "index": "vector_index",
            }
        }
    ])

    # Extract elements of the collection search
    response_list = []

    for doc in results:
        response_list.append({
            "id": doc["id"],
            "authors": doc["authors"], 
            "title": doc["title"], 
            "abstract": doc["abstract"],
            })

    search_redis_client.write(
        request=request, 
        response=SearchResponse(items=response_list)
        )

    search_postgres_client.write(
        request=request, 
        response=SearchResponse(items=response_list)
        )
    

    return SearchResponse(items=response_list)
    

@app.get("/")
def welcom_page() -> PlainTextResponse:
    return PlainTextResponse("Abstract Similarity Search..")

# query = "Markov Monte Carlo"
# for document in results:
#     print(f"Paper Title: {document['title']},\nAbstract: {document['abstract']}\n")

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8080,
        workers=1,
        reload=False
    )