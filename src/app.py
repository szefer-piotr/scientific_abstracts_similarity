from mongo.connection import collection
from utils.functions import generate_embedding

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse

import uvicorn

app = FastAPI()

@app.post("/find_similar_abstracts")
async def find_similar_abstracts(request: Request) -> JSONResponse:
    
    data = await request.json()
    query = data['query']
    
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
    response_dict = {}
    
    for doc in results:
        id, authors, title, abstract = doc["id"], doc["authors"], doc["title"], doc["abstract"]
        
        response_dict[id] = {
            "authors": authors, 
            "title": title, 
            "abstract": abstract,
            }

    return JSONResponse(response_dict)
    
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