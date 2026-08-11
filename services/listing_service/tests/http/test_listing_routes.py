from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.controllers import listings
from shared.dtos.errors import ApiErrorDTO
from shared.exceptions.exception_handlers import register_exception_handlers
from shared.exceptions.exceptions import ApiException


VALID_LISTING_PAYLOAD = {
    "title": "Downtown Apartment",
    "description": "Nice apartment near downtown",
    "price_per_night": 120.00,
    "max_guests": 4,
    "bedrooms": 2,
    "bathrooms": 1,
    "address": "123 Main St",
    "city": "New Orleans",
    "state": "LA",
    "zip_code": "70112",
}


def make_listing(**overrides):
    data = {
        "listing_id": 1,
        "host_id": 7,
        "title": "Downtown Apartment",
        "description": "Nice apartment near downtown",
        "price_per_night": 120.00,
        "max_guests": 4,
        "bedrooms": 2,
        "bathrooms": 1,
        "is_published": True,
        "address": "123 Main St",
        "city": "New Orleans",
        "state": "LA",
        "zip_code": "70112",
    }

    data.update(overrides)

    return SimpleNamespace(**data)


@pytest.fixture
def mock_listing_service():
    return Mock()


@pytest.fixture
def app(mock_listing_service):
    app = FastAPI()

    register_exception_handlers(app)
    app.include_router(listings.router)

    listings.listing_service = mock_listing_service

    return app


@pytest.fixture
def authenticated_user():
    return SimpleNamespace(
        user_id=7,
        email="john@example.com",
    )


@pytest.fixture
def client(app, authenticated_user):
    app.dependency_overrides[
        listings.get_current_user
    ] = lambda: authenticated_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def test_get_my_listings_returns_200(
    client,
    mock_listing_service,
):
    mock_listing_service.get_all_by_host_id.return_value = [
        make_listing()
    ]

    response = client.get("/api/listings/me")

    assert response.status_code == 200
    assert response.json() == [
        {
            "listing_id": 1,
            "host_id": 7,
            "title": "Downtown Apartment",
            "description": "Nice apartment near downtown",
            "price_per_night": 120.0,
            "max_guests": 4,
            "bedrooms": 2,
            "bathrooms": 1,
            "is_published": True,
            "address": "123 Main St",
            "city": "New Orleans",
            "state": "LA",
            "zip_code": "70112",
        }
    ]

    mock_listing_service.get_all_by_host_id.assert_called_once_with(7)

def test_get_my_listings_returns_empty_list(
    client,
    mock_listing_service,
):
    mock_listing_service.get_all_by_host_id.return_value = []

    response = client.get("/api/listings/me")

    assert response.status_code == 200
    assert response.json() == []

    mock_listing_service.get_all_by_host_id.assert_called_once_with(7)

def test_get_my_listings_returns_401_when_unauthenticated(
    app,
    mock_listing_service,
):
    def unauthenticated():
        raise ApiException(
            status_code=401,
            errors=[
                ApiErrorDTO(
                    message="Missing or invalid JWT."
                )
            ],
        )

    app.dependency_overrides[
        listings.get_current_user
    ] = unauthenticated

    with TestClient(app) as client:
        response = client.get("/api/listings/me")

    assert response.status_code == 401
    assert response.json() == {
        "errors": [
            {
                "message": "Missing or invalid JWT."
            }
        ]
    }

    mock_listing_service.get_all_by_host_id.assert_not_called()


def test_create_listing_returns_201(
    client,
    mock_listing_service,
):
    mock_listing_service.create_listing.return_value = make_listing()

    response = client.post(
        "/api/listings",
        json=VALID_LISTING_PAYLOAD,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["listing_id"] == 1
    assert body["host_id"] == 7
    assert body["title"] == "Downtown Apartment"
    assert body["is_published"] is True

    mock_listing_service.create_listing.assert_called_once()

    call = mock_listing_service.create_listing.call_args

    assert call.kwargs["host_id"] == 7

    dto = call.kwargs["dto"]

    assert dto.title == "Downtown Apartment"
    assert dto.price_per_night == 120.00

@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("title", ""),
        ("price_per_night", -1),
        ("max_guests", 0),
        ("bedrooms", -1),
        ("bathrooms", -1),
        ("state", "Louisiana"),
    ],
)
def test_create_listing_returns_422_for_invalid_input(
    client,
    mock_listing_service,
    field,
    value,
):
    payload = {
        **VALID_LISTING_PAYLOAD,
        field: value,
    }

    response = client.post(
        "/api/listings",
        json=payload,
    )

    assert response.status_code == 422

    mock_listing_service.create_listing.assert_not_called()