import redis
import logging

# from src.utils.errors import RedisConnectionError, RedisConnectionNotAliveError

class RedisConnector:
    """Creates and stores the connection to Redis database."""

    def __init__(self, host: str = "127.0.0.1", port: str = "6379"):
        """Initialization of redis connector.
        
        Args:
            host: Host on which redis database is working.
            port: Port to which redis database is bound to.
        """
        self.host = host
        self.port = port
        self.connection = self._create_connection(host, port)

    def close(self):
        """Closes the connection to redis database."""
        self.connection.connection_pool.disconnect(inuse_connections=True)

    def is_alive(self):
        """Checks if connection to redis database is alive."""
        self.connection.ping()

    @staticmethod
    def _create_connection(host: str, port: str):
        """Creates connection to redis database.
        
        Args:
            host: Host on which redis database is working.
            port: Port to which redis database is bound to.
        """
        connection = redis.Redis(host=host, port=port)
        connection.ping()
        return connection