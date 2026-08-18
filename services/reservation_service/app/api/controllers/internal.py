from datetime import date

from fastapi import APIRouter, Depends

from ...di.dependency_injection import get_reservation_service
from ...models.reservation import ReservationStatus


internal_router = APIRouter(
    prefix="/internal/listings",
    tags=["internal-reservations"],
)

@internal_router.get("/{listing_id}/reservations")
def get_listing_reservations(
    listing_id: int,
    status: ReservationStatus | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    service=Depends(get_reservation_service)
):
    reservations = service.find_for_listing(
        listing_id=listing_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "listing_id": listing_id,
        "reservations": reservations,
    }