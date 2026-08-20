
from datetime import date

from pydantic import BaseModel
from decimal import Decimal


class SeedUser(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class SeedUserResponse(BaseModel):
    user_id: int
    email: str
    first_name: str
    last_name: str


class SeedListing(BaseModel):
    host_id: int = 0
    title: str
    description: str
    url: str
    price_per_night: Decimal
    max_guests: int
    bedrooms: int
    bathrooms: int
    is_published: bool
    address: str
    city: str
    state: str
    zip_code: str

class SeedReservation(BaseModel):
    listing_id: int
    check_in_date: date
    check_out_date: date
    
class SeedModel():

    def __init__(
            self, 
            user: SeedUser, 
            listings: list[SeedListing], 
            reservations: list[SeedReservation]
        ):

        self.user = user
        self.listings = listings
        self.reservations = reservations
