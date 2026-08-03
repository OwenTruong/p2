from abc import ABC
import os
import logging

import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from ..utils.exceptions import UnexpectedException, DatabaseConnectionException, NoFetchedResultException, UniqueRowException
from ..dtos.db_config import DBConfig

class DBRepository(ABC):
    """Base Repository Class for Postgres Tables"""

    class __Cursor():
        """
        Provides a context manager for handling queries to our database.

        Raised Exceptions
        - DatabaseConnectionException
        - UniqueRowException
        """
        
        def __init__(self, db_config: DBConfig):
            self.__host = db_config.db_host
            self.__database = db_config.db_name
            self.__user = db_config.db_user
            self.__password = db_config.db_password
            self.__port = db_config.db_port

        def __enter__(self):
            try:
                self.connection = psycopg2.connect(
                    host=self.__host,
                    database=self.__database,
                    user=self.__user,
                    password=self.__password,
                    port=self.__port,
                )
            except psycopg2.OperationalError as e:
                logging.critical(f"Failed to establish connection to database: \n{e}\n")
                raise DatabaseConnectionException("Database backend service is unreachable.") from e

            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            return self.cursor

        def __exit__(self, exc_type, exc_val, exc_tb):
            try:
                if exc_type is None:
                    self.connection.commit()
                else:
                    self.connection.rollback()

                    if exc_type is psycopg2.errors.UniqueViolation:
                        logging.info(f"Unique constraint violated: {exc_val}")
                        raise UniqueRowException()
                    else:
                        logging.critical(
                            f"Exception occurred while executing database query: \n{exc_type}: {exc_val}\n{exc_tb}"
                    )
            finally:
                if self.cursor:
                    self.cursor.close()
                if self.connection:
                    self.connection.close()

            return False

    def __init__(self, table_name: str, table_query: str, db_config: DBConfig):
        self._table_name = table_name
        self.__db_config = db_config
        self.__ensure_table_exists(table_query)


    # TODO: Maybe add more errors/exceptions that may be thrown by psycopg2 inside method documentation

    # NOTE: using generic like "[M: BaseModel]" require Python 3.12+, generics can also be created in earlier Python but the syntax is a bit different.

    def __ensure_table_exists(self, table_query: str):
        """Initializes database schema structurally if missing
        
        Raises:
            - DatabaseConnectionException
            - UniqueRowException
        """
        with self.__Cursor(self.__db_config) as cursor:
            cursor.execute(table_query)
            logging.info(f"Schema integrity verified: {self._table_name} table is in database.")

    def _execute_fetch_one[M: BaseModel](self, query: str, model: type[M], values: list | None = None) -> M:
        """Basic protected method for fetch one queries.

        Raises:
        - DatabaseConnectionException
        - NoFetchedResultException
        - UniqueRowException
        """
        with self.__Cursor(self.__db_config) as cursor:
            cursor.execute(query, values)
            row = cursor.fetchone()
            if row is None:
                raise NoFetchedResultException("Fetched row is None after query.")
            logging.info(f"Successfully executed and fetched one row from {self._table_name}")

            return model.model_validate(row)

    def _execute_fetch_all[M: BaseModel](self, query: str, model: type[M], values: list | None = None) -> list[M]:
        """Basic protected method for fetch all queries.

        Raises:
        - DatabaseConnectionException
        - UniqueRowException
        """
        with self.__Cursor(self.__db_config) as cursor:
            cursor.execute(query, values)
            rows = cursor.fetchall()
            logging.info(f"Successfully executed and fetched rows from {self._table_name}")

            models = []

            for row in rows:
                models.append(model.model_validate(row))

            return models

    def _execute(self, query: str, values: list | None = None) -> None:
        """Basic protected method for queries that don't need any values returned.

        Raises:
        - DatabaseConnectionException
        """
        with self.__Cursor(self.__db_config) as cursor:
            cursor.execute(query, values)
            logging.info(f"Successfully executed {self._table_name}")







