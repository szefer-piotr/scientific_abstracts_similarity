from pydantic import BaseModel
from typing import List

# NestedDict: TypeAlias = dict[str, str | 'NestedDict']

class ItemModel(BaseModel):
    id: str
    authors: str 
    title: str 
    abstract: str

class SimilarAbstractsResponse(BaseModel):
    items: List[ItemModel]