from pydantic import BaseModel, Field
from src.service.schemas.base import BaseModelWithExtraConfig

class SearchRequest(BaseModelWithExtraConfig):
    query: str = Field(
        default=...,
        title="Search query.",
        description="User search query that will be embedded and used for the vector search.",
        min_length=3,
    )