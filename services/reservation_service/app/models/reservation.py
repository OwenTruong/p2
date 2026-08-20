from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class ReservationStatus(str, Enum):
    ACCEPTED = "Accepted"
    CANCELLED = "Cancelled"


class Reservation(BaseModel):
    reservation_id: int | None = None
    listing_id: int
    guest_id: int
    check_in_date: date
    check_out_date: date
    total_price: Decimal
    status: ReservationStatus = ReservationStatus.ACCEPTED