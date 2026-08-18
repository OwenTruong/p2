
from ..clients.listing_client import ListingClient
from ..services.reservation_service import ReservationService
from ..repositories.reservation_repository import ReservationRepository

def get_reservation_repository():
    return ReservationRepository()

def get_listing_client():
    return ListingClient()

def get_reservation_service():
    return ReservationService(
        reservation_repository=get_reservation_repository(),
        listing_client=get_listing_client()
    )
