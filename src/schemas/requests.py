from pydantic import BaseModel

class FindSimilarAbstractsRequest(BaseModel):
    query: str