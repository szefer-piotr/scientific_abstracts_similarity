from pydantic import Field
from typing import List
from src.service.schemas.base import BaseModelWithExtraConfig


# NestedDict: TypeAlias = dict[str, str | 'NestedDict']

class ItemModel(BaseModelWithExtraConfig):
    id: str = Field(
        default=...,
        title="Paper ID",
        description="Paper ID as it appears in the ArXiv database. It is a two, four digit string separated with a dot: 0704.0048")
    authors: str = Field(
        default=...,
        title="Authors",
        description="List of the paper authors' names and surnames."
    ) 
    title: str = Field(
        default=...,
        title="Paper title",
        description="Title of the paper."
    ) 
    abstract: str = Field(
        default=...,
        title="Abstract",
        description="Full abstract of the research paper."
    )

class SearchResponse(BaseModelWithExtraConfig):
    items: List[ItemModel] = Field(
        default=...,
        title="Similar abstract list",
        description="List of abstracts similar to the query. Number of returned abstracts is determined by the `limit` parameter (default is 4) in the aggregate function called on the vector db collection."
    )