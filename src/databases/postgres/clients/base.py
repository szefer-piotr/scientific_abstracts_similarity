from abc import ABC, abstractmethod
from psycopg2.extras import RealDictRow

from src.service.schemas.requests import SearchRequest
from src.service.schemas.responses import SearchResponse

from src.databases.postgres.connection.connector import PostgresConnector
# from src.databases.postgres.clients.search import SearchPostgresClient

from src.databases.postgres.structures.row import PostgresRow
from src.databases.postgres.structures.metadata import PostgresMetadata

from typing import TypeVar, Any

import logging

Request = TypeVar("Request", bound=SearchRequest)
Response = TypeVar("Response", bound=SearchResponse)

class BasePostgresClient(ABC):
    """Abstract class for interacting with Postgres server."""

    def __init__(self, connector: PostgresConnector, table: str):
        """Initializes the Postgres client.
        
        Args:
            connector (PostgresConnector): Connector to Postgres server.
            table (str): Name of a table to interact with."""
        self.connector = connector
        self.table = table

    def read(self, ids: list[int] | None = None) -> list[PostgresRow]:
        """Reads rows from the Postgres server.
        
        Args:
            ids (list[int]): List of ids to retrieve from the table.
            
        Returns:
            list[PostgresRow]: List of rows retrieved from the table."""
        
        query = self._prepare_selected_query(ids=ids)
        self.connector.cursor.execute(query)
        rows = self.connector.cursor.fetchall()
        prepared_rows = [self._prepare_postgres_row(row) for row in rows]
        return prepared_rows
    
    def write(self, request: Request, response: Response) -> None:
        """Saves request and response in Postgres database.
        
        Args:
            request (Request): Request object.
            response (Response): Response object."""
        
        query = self._prepare_insert_query(request, response)
        data = self._prepare_insert_data(request, response)
        self.connector.cursor.execute(query, data)
        self.connector.connection.commit()

    @abstractmethod
    def _prepare_request(self, raw_postgres_row: RealDictRow) -> Request:
        """Prepares request object from raw Postgres row.
        
        Args:
            raw_postgres_row (RealDictRow): Raw Postgres row.
            
        Returns:
            Request: Transformed and prepared Request object."""
        
        raise NotImplementedError

    @abstractmethod
    def _prepare_response(self, raw_postgres_row: RealDictRow) -> Response:
        """Prepares response object from raw Postgres row.
        
        Args:
            raw_postgres_row (RealDictRow): Raw Postgres row.
            
        Returns:
            Response: Transformed and prepared Response object."""
        
        raise NotImplementedError

    def _prepare_metadata(self, raw_postgres_row: RealDictRow) -> PostgresMetadata:
        """Prepares metadata object from raw Postgres row.
        
        Args:
            raw_postgres_row (RealDictRow): Raw Postgres row.
            
        Returns:
            Transformed and prepared metadata object."""
        fields = PostgresMetadata.__fields__.keys()
        metadata = self._extract_data(raw_postgres_row, fields)
        return PostgresMetadata(**metadata)

    def _prepare_postgres_row(self, raw_postgres_row: RealDictRow) -> PostgresRow:
        """Prepares Postgres row object from raw Postgres row.
        
        Args:
            raw_postgres_row (RealDictRow): Raw Postgres row.
            
        Returns:
            PostgresRow: Transformed and prepared Postgres row object."""
        
        metadata = self._prepare_metadata(raw_postgres_row)
        request = self._prepare_request(raw_postgres_row)
        response = self._prepare_response(raw_postgres_row)
        return PostgresRow(request=request, response=response, metadata=metadata)

    @staticmethod
    def _extract_data(raw_postgres_row: RealDictRow, fields: list[str]) -> dict[str, Any]:
        """Extracts data from raw Postgres row.
        
        Args:
            raw_postgres_row (RealDictRow): Raw Postgres row.
            fields (list[str]): List of fields to extract.
            
        Returns:
            dict[str, Any]: Extracted data."""
        
        return {field: raw_postgres_row[field] for field in fields} 

    def _prepare_insert_query(self, request: Request, response: Response) -> str:
        """Prepares query for inserting data into Postgres table.
        
        Args:
            request (Request): Request object.
            response (Response): Response object.
            
        Returns:
            str: Prepared query."""
        
        request_fields = list(request.model_dump().keys())
        response_fields = list(response.model_dump().keys())
        all_fields = request_fields + response_fields
        query = "INSERT INTO "
        query += f"{self.table} "
        query += "(" + ", ".join(all_fields) + ") "
        query += "VALUES "
        query += "(" + ", ".join(["%s" for _ in range(len(all_fields))]) + ") "
        return query

    @staticmethod
    def _prepare_insert_data(request: Request, response: Response) -> list[Any]:
        """Prepares data for inserting into Postgres table.
        
        Args:
            request (Request): Request object.
            response (Response): Response object.
            
        Returns:
            tuple: Prepared data."""
        
        request_data = tuple(request.model_dump().values())
        response_data = tuple(response.model_dump().values())
        return request_data + response_data

    def _prepare_select_query(self, ids: list[int] | None = None) -> str:
        """Prepares query for selecting data from Postgres table.
        
        Args:
            ids (list[int]): List of ids to retrieve.
            
        Returns:
            str: Prepared query."""
        
        ids = [ids] if ids is not None and not isinstance(ids, list) else ids
        query = f"SELECT * FROM {self.table}"
        if ids is not None:
            query += f" WHERE id in ({', '.join([str(id_) for id_ in ids])})"
        return query
