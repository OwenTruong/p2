# tests/integration/test_user_schema.py

import psycopg2
import pytest
from psycopg2.extensions import connection


def test_user_id_is_generated_by_database(
    db_connection: connection,
) -> None:
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO users (
                email,
                password_hash,
                first_name,
                last_name
            )
            VALUES (%s, %s, %s, %s)
            RETURNING user_id
            """,
            (
                "generated@example.com",
                "hash",
                "John",
                "Doe",
            ),
        )

        row = cursor.fetchone()

    db_connection.commit()

    assert row is not None
    assert row[0] >= 1


def test_email_cannot_be_null(
    db_connection: connection,
) -> None:
    with pytest.raises(psycopg2.errors.NotNullViolation):
        with db_connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (
                    email,
                    password_hash,
                    first_name,
                    last_name
                )
                VALUES (NULL, %s, %s, %s)
                """,
                ("hash", "John", "Doe"),
            )

    db_connection.rollback()


def test_email_must_be_unique(
    db_connection: connection,
) -> None:
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO users (
                email,
                password_hash,
                first_name,
                last_name
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                "duplicate@example.com",
                "hash",
                "John",
                "Doe",
            ),
        )

    db_connection.commit()

    with pytest.raises(psycopg2.errors.UniqueViolation):
        with db_connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (
                    email,
                    password_hash,
                    first_name,
                    last_name
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    "duplicate@example.com",
                    "another-hash",
                    "Jane",
                    "Doe",
                ),
            )

    db_connection.rollback()


def test_required_name_cannot_be_null(
    db_connection: connection,
) -> None:
    with pytest.raises(psycopg2.errors.NotNullViolation):
        with db_connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (
                    email,
                    password_hash,
                    first_name,
                    last_name
                )
                VALUES (%s, %s, NULL, %s)
                """,
                (
                    "missing-name@example.com",
                    "hash",
                    "Doe",
                ),
            )

    db_connection.rollback()


def test_invalid_status_is_rejected(
    db_connection: connection,
) -> None:
    with pytest.raises(
        (
            psycopg2.errors.InvalidTextRepresentation,
            psycopg2.errors.CheckViolation,
        )
    ):
        with db_connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (
                    email,
                    password_hash,
                    first_name,
                    last_name,
                    status
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    "invalid-status@example.com",
                    "hash",
                    "John",
                    "Doe",
                    "Deleted",
                ),
            )

    db_connection.rollback()