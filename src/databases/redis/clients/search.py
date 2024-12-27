import pickle
from src.service.schemas.responses import SearchResponse
from src.databases.redis.clients.base import BaseRedisClient

class SearchRedisClient(BaseRedisClient):
    """Client that handles the search results returned from vector search."""
    
    @staticmethod
    def _create_value(response: SearchResponse) -> bytes:
        return pickle.dumps(response.items)
    
    @staticmethod
    def _create_response(value: bytes) -> SearchResponse:
        """Creates a decision response from value retrieved from Redis database.
        
        Args:
            value (bytes): Value retrieved from Redis database.
            
        Returns:
            SearchResponse: Response object."""
        return SearchResponse(items=pickle.loads(value))