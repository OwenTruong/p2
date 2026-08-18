from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.api.controllers import auth
from shared.exceptions.exception_handlers import register_exception_handlers
from shared.exceptions.exceptions import EmailAlreadyExistsException
from shared.utils.exceptions import UniqueRowException

@pytest.fixture
def mock_auth_service():
    return Mock()

@pytest.fixture
def client(mock_auth_service):
    app = FastAPI()
    app.include_router(auth.router)

    register_exception_handlers(app)

    app.dependency_overrides[auth.get_auth_service] = (
        lambda: mock_auth_service
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def test_register_returns_201(client, mock_auth_service):
    mock_auth_service.save_user.return_value = SimpleNamespace(
        user_id=1,
        email="john@example.com",
        first_name="John",
        last_name="Doe",
        status="Active"
    )

    response = client.post(
        "/api/auth/register",
        json={
            "email": "john@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "user_id": 1,
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "status": "Active"
    }

    mock_auth_service.save_user.assert_called_once()

    dto = mock_auth_service.save_user.call_args.args[0]

    assert dto.email == "john@example.com"
    assert dto.first_name == "John"
    assert dto.last_name == "Doe"

def test_register_returns_409_when_email_exists(
    client, mock_auth_service
):
    mock_auth_service.save_user.side_effect = EmailAlreadyExistsException()

    response = client.post(
        "/api/auth/register",
        json={
            "email": "john@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
        }
    )

    assert response.status_code == 409
    assert response.json() == {
        "errors": [
            {
                "message": "User with this email already exists."
            }
        ]
    }

def test_register_returns_422_for_invalid_request(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "not-an-email",
            "password": "short",
            "first_name": "J",
            "last_name": "Doe",
        },
    )

    assert response.status_code == 422

def test_login_returns_200_and_sets_access_token_cookie(
    client, mock_auth_service
):
    mock_user = SimpleNamespace(
        email="john@example.com",
    )

    mock_auth_service.authenticate_user.return_value = (
        mock_user,
        "jwt-token",
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert response.cookies.get("access_token") == "jwt-token"

    set_cookie = response.headers["set-cookie"]

    assert "access_token=jwt-token" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "SameSite=lax" in set_cookie
    assert "Path=/" in set_cookie

    mock_auth_service.authenticate_user.assert_called_once()

    dto = mock_auth_service.authenticate_user.call_args.args[0]

    assert dto.email == "john@example.com"
    assert dto.password == "password123"

def test_login_returns_401_for_invalid_credentials(
    client, mock_auth_service
):

    mock_auth_service.authenticate_user.side_effect = HTTPException(
        status_code=401,
        detail="invalid credentials",
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "invalid credentials"
    }

    assert response.cookies.get("access_token") is None

def test_login_returns_403_for_inactive_account(
    client, mock_auth_service
):

    mock_auth_service.authenticate_user.side_effect = HTTPException(
        status_code=403,
        detail="account is inactive",
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "account is inactive"
    }

def test_logout_deletes_access_token_cookie(
    client, mock_auth_service
):
    mock_auth_service.authenticate_user.return_value = (
        "",
        "jwt-token",
    )

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200
    assert client.cookies.get("access_token") == "jwt-token"

    logout_response = client.post("/api/auth/logout")

    assert logout_response.status_code == 200
    assert client.cookies.get("access_token") is None

    set_cookie = logout_response.headers["set-cookie"]
    assert "access_token=" in set_cookie
    assert "Max-Age=0" in set_cookie
    assert "Path=/" in set_cookie