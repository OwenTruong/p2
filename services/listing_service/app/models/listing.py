from pydantic import BaseModel, Field
from typing import Literal

class Listing(BaseModel):
    listing_id: int | None = Field(default=None, ge=1)
    host_id: int = Field(ge=1)
    title: str = Field(examples=["Cozy Downtown Apartment"], min_length=1, max_length=128)
    description: str = Field(min_length=1, max_length=1024)
    location: str = Field(examples=["New York, NY"], min_length=1, max_length=256)
    price_per_night: float = Field(gt=0, examples=[120.00])
    max_guests: int = Field(ge=1, examples=[4])
    bedrooms: int = Field(ge=0, examples=[2])
    bathrooms: int = Field(ge=0, examples=[1])
    status: Literal["Available", "Unavailable"] = Field(default="Available", examples=["Available"])