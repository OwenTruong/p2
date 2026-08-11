
from collections.abc import Generator

import pytest

from app.models.listing import Listing
from app.repositories.listing_repository import ListingRepository


def make_listing(
    *,
    host_id: int = 7,
    title: str = "Downtown Apartment",
) -> Listing:
    return Listing(
        listing_id=None,
        host_id=host_id,
        title=title,
        description="Nice apartment near downtown",
        price_per_night=120.00,
        max_guests=4,
        bedrooms=2,
        bathrooms=1,
        is_published=True,
        address="123 Main St",
        city="New Orleans",
        state="LA",
        zip_code="70112",
    )

def test_save_persists_listing() -> None:
    repository = ListingRepository()

    created = repository.save(
        make_listing()
    )

    assert created.listing_id == 1
    assert created.host_id == 7
    assert created.title == "Downtown Apartment"
    assert created.description == "Nice apartment near downtown"
    assert float(created.price_per_night) == 120.00
    assert created.max_guests == 4
    assert created.bedrooms == 2
    assert created.bathrooms == 1
    assert created.is_published is True
    assert created.city == "New Orleans"
    assert created.state == "LA"


def test_find_all_by_host_id_returns_only_that_hosts_listings() -> None:
    repository = ListingRepository()

    repository.save(
        make_listing(
            host_id=7,
            title="Host Seven Listing One",
        )
    )

    repository.save(
        make_listing(
            host_id=7,
            title="Host Seven Listing Two",
        )
    )

    repository.save(
        make_listing(
            host_id=8,
            title="Host Eight Listing",
        )
    )

    result = repository.find_all_by_host_id(7)

    assert len(result) == 2

    assert all(
        listing.host_id == 7
        for listing in result
    )

    titles = {
        listing.title
        for listing in result
    }

    assert titles == {
        "Host Seven Listing One",
        "Host Seven Listing Two",
    }

def test_find_all_by_host_id_returns_empty_list_when_none_exist() -> None:
    repository = ListingRepository()

    result = repository.find_all_by_host_id(999)

    assert result == []


def test_database_generates_unique_listing_ids() -> None:
    repository = ListingRepository()

    first = repository.save(
        make_listing(
            host_id=7,
            title="First Listing",
        )
    )

    second = repository.save(
        make_listing(
            host_id=7,
            title="Second Listing",
        )
    )

    assert first.listing_id == 1
    assert second.listing_id == 2
    assert first.listing_id != second.listing_id