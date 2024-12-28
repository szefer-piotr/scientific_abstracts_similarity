import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# from src.utils.errors import PostgresConnectionError

class PostgresConnector:
    """Creates a connection to a Postgres database."""

    def __init__(
        self,
        host: str = "127.0.0.1", 
        port: str = "5432", 
        database: str = "monitoring",
        user: str = "postgres", 
        password: str = "12345",
    ):
        self.connection = self._create_connection(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        self.cursor = self._create_cursor(self.connection)
    
    def close(self):
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def _create_connection( 
        host: str, 
        port: str,
        database: str, 
        user: str, 
        password: str,
    ) -> psycopg2.extensions.connection:
        """"Initialization of connection to Postgres database.
        
        Args:
            host (str): Host of Postgres database.
            port (str): Port of Postgres database.
            database (str): Name of the database.
            user (str): Username.
            password (str): Password.
        
        Return:
            psycopg2.extensions.connection: Connection to Postgres database."""
        logging.info(f"Connecting to Postgres database on {database=}, {user=}, {host=}, {port=}.")
        try:
            connection = psycopg2.connect(
                database=database,
                user=user,
                password=password,
                host=host,
                port=port,
            )
        except psycopg2.OperationalError as e:
            logging.error(f"Error connecting to Postgres: {e}")
            # raise PostgresConnectionError(database, user, host, port) from e
        logging.info("Connected to Postgres database.")
        return connection
    
    @staticmethod
    def _create_cursor(
        connection: psycopg2.extensions.connection
    ) -> psycopg2.extensions.cursor:
    
        """Initialization of cursor for Postgres database.
        
        Args:
            connection (psycopg2.extensions.connection): Connection to Postgres database.
        
        Return:
            psycopg2.extensions.cursor: Cursor for Postgres database."""
        
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        return cursor