from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.dtos.auth import LoginRequest
from app.dtos.user_dto import UserCreateRequestDTO, UserResponseDTO
from app.services.auth_service import AuthService
from shared.dtos.errors import ApiErrorDTO
from shared.exceptions.exceptions import ApiException

def test_authenticate_user_returns_user_and_token():

    #########
    # ARRANGE 
    #########

    repository = Mock()

    stored_user = SimpleNamespace(
        user_id=1,
        email="john@example.com",
        password_hash="stored-hash",
        status="Active",
    )

    repository.find_by_email.return_value = stored_user
    service = AuthService(user_repo=repository)

    dto = LoginRequest(
        email="john@example.com",
        password="password123",
    )

    #########
    # ACT
    #########
    
    with (
        patch(
            "app.services.auth_service.verify_password",
            return_value=True,
        ) as mock_verify,
        patch(
            "app.services.auth_service.create_access_token",
            return_value="jwt-token",
        ) as mock_create_token,
    ):
        user, token = service.authenticate_user(dto)

    #########
    # ASSERT
    #########

    # Assert results
    assert user is stored_user
    assert token == "jwt-token"

    # Assert interactions with mocks
    repository.find_by_email.assert_called_once_with("john@example.com")
    mock_verify.assert_called_once_with("password123", "stored-hash")
    mock_create_token.assert_called_once_with(1, "john@example.com")

def test_authenticate_user_raises_401_when_user_not_found():
    repository = Mock()
    repository.find_by_email.return_value = None

    service = AuthService(user_repo=repository)

    dto = LoginRequest(
        email="missing@example.com",
        password="password123",
    )

    with pytest.raises(ApiException) as exc_info:
        service.authenticate_user(dto)

    assert exc_info.value.status_code == 401
    assert exc_info.value.errors == [
            ApiErrorDTO(message="Invalid email or password.")
    ]
                
    
    repository.find_by_email.assert_called_once_with(
        "missing@example.com"
    )

def test_authenticate_user_raises_401_when_password_is_invalid():
    repository = Mock()

    stored_user = SimpleNamespace(
        email="john@example.com",
        password_hash="stored-hash",
        status="Active",
    )

    repository.find_by_email.return_value = stored_user
    service = AuthService(user_repo=repository)

    dto = LoginRequest(
        email="john@example.com",
        password="wrong-password",
    )

    with patch(
        "app.services.auth_service.verify_password",
        return_value=False,
    ) as mock_verify:
        with pytest.raises(ApiException) as exc_info:
            service.authenticate_user(dto)

    assert exc_info.value.status_code == 401
    assert exc_info.value.errors == [
            ApiErrorDTO(message="Invalid email or password.")
    ]
    
    mock_verify.assert_called_once_with(
        "wrong-password",
        "stored-hash",
    )

def test_authenticate_user_raises_403_when_account_is_inactive():
    repository = Mock()

    stored_user = SimpleNamespace(
        email="john@example.com",
        password_hash="stored-hash",
        status="Inactive",
    )

    repository.find_by_email.return_value = stored_user
    service = AuthService(user_repo=repository)

    dto = LoginRequest(
        email="john@example.com",
        password="password123",
    )

    with patch(
        "app.services.auth_service.verify_password",
        return_value=True,
    ):
        with pytest.raises(ApiException) as exc_info:
            service.authenticate_user(dto)

    assert exc_info.value.status_code == 403
    assert exc_info.value.errors == [
            ApiErrorDTO(message="Account is inactive.")
    ]

def test_save_user_hashes_password_and_saves_user():
    repository = Mock()

    saved_user = SimpleNamespace(
        user_id=1,
        email="john@example.com",
        first_name="John",
        last_name="Doe",
        status="Active"
    )

    repository.save.return_value = saved_user
    service = AuthService(user_repo=repository)

    dto = UserCreateRequestDTO(
        email="john@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
    )

    with patch(
        "app.services.auth_service.hash_password",
        return_value="hashed-password",
    ) as mock_hash:
        result = service.save_user(dto)

    mock_hash.assert_called_once_with("password123")
    repository.save.assert_called_once()

    user_passed_to_repository = repository.save.call_args.args[0]
    
    assert isinstance(result, UserResponseDTO)
    assert user_passed_to_repository.email == "john@example.com"
    assert user_passed_to_repository.password_hash == "hashed-password"
    assert user_passed_to_repository.first_name == "John"
    assert user_passed_to_repository.last_name == "Doe"