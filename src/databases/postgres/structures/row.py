from __future__ import annotations

from pydantic import BaseModel, Field
from psycopg2.extras import RealDictRow

from src.service.schemas.requests import SearchRequest
from src.service.schemas.responses import SearchResponse
from src.databases.postgres.structures.metadata import PostgresMetadata

class PostgresRow(BaseModel):
    """Datastructure to represent postgres row."""

    class Config:
        extra = "forbid"

    metadata: PostgresMetadata = Field(
        default=..., 
        title="Metadata",
        description="Metadata of the record.",
        )
    
    request: SearchRequest = Field(
        default=...,
        title="Request",
        description="Request object.",
        )
    
    response: SearchResponse = Field(
        default=...,
        title="Response",
        description="Response object.",
        )