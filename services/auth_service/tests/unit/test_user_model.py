# tests/unit/test_user_model.py

import pytest
from pydantic import ValidationError

from app.models.user import User


def valid_user_data() -> dict:
    return {
        "user_id": 1,
        "email": "john@example.com",
        "password_hash": "hashed-password-value",
        "first_name": "John",
        "last_name": "Doe",
        "status": "Active",
    }


def test_create_valid_user() -> None:
    user = User(**valid_user_data())

    assert user.user_id == 1
    assert user.email == "john@example.com"
    assert user.password_hash == "hashed-password-value"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.status == "Active"


def test_new_user_may_have_no_id() -> None:
    data = valid_user_data()
    data.pop("user_id")

    user = User(**data)

    assert user.user_id is None


def test_status_defaults_to_active() -> None:
    data = valid_user_data()
    data.pop("status")

    user = User(**data)

    assert user.status == "Active"


@pytest.mark.parametrize("status", ["Active", "Inactive"])
def test_accepts_valid_statuses(status: str) -> None:
    data = valid_user_data()
    data["status"] = status

    user = User(**data)

    assert user.status == status


def test_rejects_invalid_status() -> None:
    data = valid_user_data()
    data["status"] = "Deleted"

    with pytest.raises(ValidationError):
        User(**data)


@pytest.mark.parametrize(
    "email",
    [
        "not-an-email",
        "john@",
        "@example.com",
        "",
    ],
)
def test_rejects_invalid_email(email: str) -> None:
    data = valid_user_data()
    data["email"] = email

    with pytest.raises(ValidationError):
        User(**data)


@pytest.mark.parametrize("field_name", ["first_name", "last_name"])
def test_rejects_empty_names(field_name: str) -> None:
    data = valid_user_data()
    data[field_name] = ""

    with pytest.raises(ValidationError):
        User(**data)


def test_rejects_empty_password_hash() -> None:
    data = valid_user_data()
    data["password_hash"] = ""

    with pytest.raises(ValidationError):
        User(**data)


@pytest.mark.parametrize("user_id", [0, -1])
def test_rejects_non_positive_user_id(user_id: int) -> None:
    data = valid_user_data()
    data["user_id"] = user_id

    with pytest.raises(ValidationError):
        User(**data)


def test_serializes_user_to_dictionary() -> None:
    user = User(**valid_user_data())

    result = user.model_dump()

    assert result == valid_user_data()


def test_rejects_missing_required_field() -> None:
    data = valid_user_data()
    data.pop("email")

    with pytest.raises(ValidationError):
        User(**data)