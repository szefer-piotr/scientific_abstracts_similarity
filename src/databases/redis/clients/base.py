from abc import ABC, abstractmethod

from src.service.schemas.requests import SearchRequest
from src.service.schemas.responses import SearchResponse
from src.databases.redis.connection.connector import RedisConnector
from typing import TypeVar
import logging

Request = TypeVar("Request", bound=SearchRequest)
Response = TypeVar("Response", bound=SearchResponse)

class BaseRedisClient(ABC):
    """Abstract base class for interaacting with Redis server."""
    def __init__(self, connector: RedisConnector):
        """Initialization of redis client.
        
        Args:
            connector (RedisConnector): Instance of RedisConnector.
        """
        self.connector = connector

    def read(self, request: Request) -> Response:
        """Read data from Redis server.
        
        Args:
            request (Request): Request object.
            
        Returns:
            Response: Response object.
        """
        logging.info(f"Getting response from Redis for {request=}")
        self.connector.is_alive()
        key = self._create_key(request=request)
        value = self.connector.connection.get(key)
        if value:
            response = self._create_response(value)
            logging.info(f"Response from Redis: {response=}")
            return response
        else:
            logging.info("Response not available in Redis.")
            return None
        
    def write(self, request: Request, response: Response) -> None:
        """Saves response to Redis server.
        
        Args:
            request (Request): Request for which we want to save response in redis database.
            response (Response): Response for a given request which we want to save in redis database.
        """
        logging.info(f"Saving {response=} in Redis for {request=}")
        self.connector.is_alive()
        key = self._create_key(request=request)
        value = self._create_value(response)
        self.connector.connection.set(key, value)
        logging.info("Response saved in Redis.")

    # @staticmethod
    def _create_key(self, request: Request) -> str:
        """Creates key for Redis database.
        
        Args:
            request (Request): Request object.
            
        Returns:
            str: Key for Redis database.
        """
        return repr(request)
    
    @staticmethod
    @abstractmethod
    def _create_value(response: Response) -> str:
        """Creates value for Redis database.
        
        Args:
            response (Response): Response object.
            
        Returns:
            str: Value for Redis database.
        """
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def _create_response(value: bytes) -> Response:
        """Creates response object from value.
        
        Args:
            value (bytes): Value from Redis database.
            
        Returns:
            Response: Response object.
        """
        raise NotImplementedError