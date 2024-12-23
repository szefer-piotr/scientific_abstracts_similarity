from mongo.connection import collection
from utils.functions import generate_embedding

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from src.schemas.requests import FindSimilarAbstractsRequest
from src.schemas.responses import SimilarAbstractsResponse

import uvicorn

app = FastAPI()

@app.post("/find_similar_abstracts")
def find_similar_abstracts(
    request: FindSimilarAbstractsRequest
    ) -> SimilarAbstractsResponse:
    
    query = request.model_dump()['query']
    # breakpoint()
    results = collection.aggregate([
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
        
    # breakpoint()
    return SimilarAbstractsResponse(items=response_list)
    # return SimilarAbstractsResponse(**{"items": response_list})
    
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