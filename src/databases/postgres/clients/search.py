from psycopg2.extras import RealDictRow

from src.databases.postgres.connection.connector import PostgresConnector
from src.databases.postgres.clients.base import BasePostgresClient

from src.service.schemas.requests import SearchRequest
from src.service.schemas.responses import SearchResponse

class SearchPostgresClient(BasePostgresClient):
    """Base class for interacting with Postgres server for search purposes."""

    def __init__(self, connector: PostgresConnector, table: str = "search_results"):
        """Initializes the Postgres client.
        
        Args:
            connector (PostgresConnector): Connector to Postgres server.
            table (str): Name of a table to interact with."""
        super().__init__(connector=connector, table=table)

    def _prepare_request(self, raw_postgres_row: RealDictRow) -> SearchRequest:
        """Prepares request object from raw Postgres row.
        
        Args:
            raw_postgres_row (RealDictRow): Raw Postgres row.
            
        Returns:
            SearchRequest: Request object."""
        fields = SearchRequest.model_fields.keys()
        request_data = self._extract_data(raw_postgres_row, fields)
        return SearchRequest(**request_data)
    
    def _prepare_response(self, raw_postgres_row: RealDictRow) -> SearchResponse:
        """Prepares response object from raw Postgres row.
        
        Args:
            raw_postgres_row (RealDictRow): Raw Postgres row.
            
        Returns:
            SearchResponse: Response object."""
        fields = SearchResponse.model_fields.keys()
        response_data = self._extract_data(raw_postgres_row, fields)
        return SearchResponse(**response_data)