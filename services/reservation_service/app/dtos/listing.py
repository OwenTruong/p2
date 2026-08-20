from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ListingResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    listing_id: int
    host_id: int
    title: str
    description: str | None
    price_per_night: Decimal
    max_guests: int
    bedrooms: int
    bathrooms: int
    is_published: bool
    address: str
    city: str
    state: str
    zip_code: str