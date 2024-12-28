from pydantic import BaseModel, Field
import datetime

class PostgresMetadata(BaseModel):
    """Datastructure to represent postgres metadata.
    
    Postgres metadata is interpreted as: all other information stored in table
    that is not data passed to the model as input nor output from the model"""

    class Config:
        extra = "forbid"

    id: int = Field(
        default=..., 
        title="ID",
        description="Unique identifier of the record.",
        )
    
    timestamp: datetime.datetime = Field(
        default=...,
        title="Timestamp",
        description="Timestamp of the record creation.",
        )
