# tests/integration/conftest.py

import os
from collections.abc import Generator

import psycopg2
import pytest
from psycopg2.extensions import connection


@pytest.fixture(scope="session")
def database_url() -> str:
    return os.getenv(
        "TEST_DATABASE_URL",
        (
            "postgresql://postgres:postgres"
            "@localhost:5433/auth_test_db"
        ),
    )


@pytest.fixture
def db_connection(
    database_url: str,
) -> Generator[connection, None, None]:
    db = psycopg2.connect(database_url)

    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(autouse=True)
def clean_users_table(
    db_connection: connection,
) -> Generator[None, None, None]:
    with db_connection.cursor() as cursor:
        cursor.execute(
            "TRUNCATE TABLE users RESTART IDENTITY CASCADE"
        )

    db_connection.commit()

    yield

    with db_connection.cursor() as cursor:
        cursor.execute(
            "TRUNCATE TABLE users RESTART IDENTITY CASCADE"
        )

    db_connection.commit()