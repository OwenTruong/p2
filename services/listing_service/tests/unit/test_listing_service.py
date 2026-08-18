
from unittest.mock import Mock, MagicMock
from decimal import Decimal

from app.dtos.listing import ListingCreateRequestDTO
from app.models.listing import Listing
from app.services.listing_service import ListingService


def make_create_dto() -> ListingCreateRequestDTO:
    return ListingCreateRequestDTO(
        title="Downtown Apartment",
        description="Nice apartment near downtown",
        price_per_night=Decimal(120.00),
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
        price_per_night=Decimal(120.00),
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
    assert listing.price_per_night == Decimal(120.00)
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

def test_delete_listing__normal() -> None:
    # Define constants for the mock
    valid_listing = Listing(
        listing_id = 100,
        host_id = 1,
        title = "APA Hotel Ueno",
        description = "Affordable Hotel for Tourists",
        price_per_night = Decimal(80.00),
        max_guests = 4,
        bedrooms = 4,
        bathrooms = 2,
        is_published = True,
        address = "Somewhere in Ueno",
        city = "Ueno",
        state = "Tokyo",
        zip_code = "11111"
    )

    # Define the mocked repository
    listing_repository = MagicMock()
    listing_repository.find_by_id.return_value = valid_listing
    listing_repository.save.side_effect = lambda x: x

    # Run the service
    service = ListingService(listing_repository)
    result = service.delete_listing(1, 100)

    # Post-run repository info
    listing_repository.find_by_id.assert_called_once_with(100)
    listing_repository.save.assert_called_once()
    saved_listing = listing_repository.save.call_args.args[0]

    # Assert that the method actually ran save() with the correct listing
    assert saved_listing.listing_id == 100
    # Assert that result was actually returned
    assert result
    # Assert that it was soft deleted
    assert result.is_published == False


