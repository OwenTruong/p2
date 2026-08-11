
from unittest.mock import Mock

from app.dtos.listing import ListingCreateRequestDTO
from app.models.listing import Listing
from app.services.listing_service import ListingService


def make_create_dto() -> ListingCreateRequestDTO:
    return ListingCreateRequestDTO(
        title="Downtown Apartment",
        description="Nice apartment near downtown",
        price_per_night=120.00,
        max_guests=4,
        bedrooms=2,
        bathrooms=1,
        address="123 Main St",
        city="New Orleans",
        state="LA",
        zip_code="70112",
    )


def test_create_listing_maps_dto_and_saves_listing() -> None:
    repository = Mock()
    service = ListingService(repository)

    dto = ListingCreateRequestDTO(
        title="Downtown Apartment",
        description="Nice apartment near downtown",
        price_per_night=120.00,
        max_guests=4,
        bedrooms=2,
        bathrooms=1,
        address="123 Main St",
        city="New Orleans",
        state="LA",
        zip_code="70112",
    )

    saved_listing = Mock()
    repository.save.return_value = saved_listing

    result = service.create_listing(
        host_id=7,
        dto=dto,
    )

    repository.save.assert_called_once()

    listing = repository.save.call_args.args[0]

    assert listing.listing_id is None
    assert listing.host_id == 7
    assert listing.title == "Downtown Apartment"
    assert listing.description == "Nice apartment near downtown"
    assert listing.price_per_night == 120.00
    assert listing.max_guests == 4
    assert listing.bedrooms == 2
    assert listing.bathrooms == 1
    assert listing.is_published is True
    assert listing.address == "123 Main St"
    assert listing.city == "New Orleans"
    assert listing.state == "LA"
    assert listing.zip_code == "70112"

    assert result is saved_listing


def test_get_all_by_host_id_delegates_to_repository() -> None:
    repository = Mock()
    service = ListingService(repository)

    listings = [
        Mock(host_id=7),
        Mock(host_id=7),
    ]

    repository.find_all_by_host_id.return_value = listings

    result = service.get_all_by_host_id(7)

    repository.find_all_by_host_id.assert_called_once_with(7)
    assert result == listings