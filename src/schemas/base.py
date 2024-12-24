from pydantic import BaseModel

class BaseModelWithExtraConfig(BaseModel):
    class Config:
        extra = "forbid"