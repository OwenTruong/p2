from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from ..models.reservation import ReservationStatus

class CreateReservationRequest(BaseModel):
    listing_id: int
    check_in_date: date
    check_out_date: date

class CreateReservationResponse(BaseModel):
    reservation_id: int | None = None
    listing_id: int
    guest_id: int
    check_in_date: date
    check_out_date: date
    total_price: Decimal
    status: ReservationStatus

class ReservationResponse(BaseModel):
    reservation_id: int | None = None
    listing_id: int
    guest_id: int
    check_in_date: date
    check_out_date: date
    total_price: Decimal
    status: ReservationStatus
    
class UpdateReservationRequest(BaseModel):
    check_in_date: date
    check_out_date: date