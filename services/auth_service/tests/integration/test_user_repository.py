# tests/integration/test_user_repository.py

import pytest

from app.repositories.user_repository import UserRepository
from services.auth_service.app.models.user import User
from shared.utils.exceptions import UniqueRowException


def make_user(
    email: str = "john@example.com",
) -> User:
    return User(
        email=email,
        password_hash="example-password-hash",
        first_name="John",
        last_name="Doe",
    )


def test_create_user_persists_record() -> None:
    repository = UserRepository()

    created = repository.save(make_user())

    assert created.user_id == 1
    assert created.email == "john@example.com"
    assert created.password_hash == "example-password-hash"
    assert created.first_name == "John"
    assert created.last_name == "Doe"
    assert created.status == "Active"


def test_get_user_by_id() -> None:
    repository = UserRepository()
    created = repository.save(make_user())

    found = repository.find_by_id(created.user_id)

    assert found is not None
    assert found.user_id == created.user_id
    assert found.email == created.email


def test_missing_user_returns_none() -> None:
    repository = UserRepository()

    found = repository.find_by_id(99999)

    assert found is None


def test_get_user_by_email() -> None:
    repository = UserRepository()
    repository.save(make_user())

    found = repository.find_by_email("john@example.com")

    assert found is not None
    assert found.email == "john@example.com"


def test_database_generates_sequential_ids() -> None:
    repository = UserRepository()

    first = repository.save(
        make_user("first@example.com")
    )
    second = repository.save(
        make_user("second@example.com")
    )

    assert first.user_id == 1
    assert second.user_id == 2


def test_duplicate_email_is_rejected() -> None:
    repository = UserRepository()
    repository.save(make_user())

    with pytest.raises(UniqueRowException):
        repository.save(make_user())


def test_status_defaults_to_active() -> None:
    repository = UserRepository()

    created = repository.save(make_user())

    assert created.status == "Active"


def test_update_user_status() -> None:
    repository = UserRepository()
    created = repository.save(make_user())

    updated = repository.update_status(
        created.user_id,
        "Inactive",
    )

    assert updated is not None
    assert updated.status == "Inactive"

    persisted = repository.find_by_id(created.user_id)

    assert persisted is not None
    assert persisted.status == "Inactive"