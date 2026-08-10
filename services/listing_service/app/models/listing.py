from decimal import Decimal

from pydantic import BaseModel, Field
from typing import Literal

class Listing(BaseModel):
    listing_id: int | None = Field(default=None, ge=1)
    host_id: int = Field(ge=1)
    title: str = Field(examples=["Cozy Downtown Apartment"], min_length=1, max_length=128)
    description: str = Field(min_length=1, max_length=1024)
    price_per_night: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
        examples=[Decimal("125.00")],
        )
    max_guests: int = Field(ge=1, examples=[4])
    bedrooms: int = Field(ge=0, examples=[2])
    bathrooms: int = Field(ge=0, examples=[1])
    is_published: bool = True
    address: str
    city: str
    state: str
    zip_code: str
