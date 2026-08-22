from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator
import re

class ListingCreateRequestDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=256, examples=["Downtown Apartment"])
    description: str = Field(default=None, max_length=512, examples=["Two-bedroom apartment near downtown."])
    url: str = Field(default=None, max_length=512, examples=["https://images.squarespace-cdn.com/content/v1/6671cdf4eb7de91f577a464e/1760034971967-ZUG8QSHUXLKIZOEGRV14/The+Risks+of+Overpricing_+What+Owasso+Homeowners+Should+Know+1.png"])
    price_per_night: Decimal = Field(gt=0, max_digits=10, decimal_places=2, examples=[Decimal("125.00")],)
    max_guests: int = Field(..., gt=0, examples=[4])
    bedrooms: int = Field(..., gt=0, examples=[2])
    bathrooms: int = Field(..., gt=0, examples=[1])
    address: str = Field(..., min_length=1, max_length=150, examples=["100 Main Street"])
    city: str = Field(..., min_length=1, max_length=100, examples=["New Orleans"])
    state: str = Field(..., examples=["LA"])
    zip_code: str = Field(..., examples=["70112"])
    is_published: bool
    
    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        v_upper = v.strip().upper()
        if not re.match(r"^[A-Z]{2}$", v_upper):
            raise ValueError("State must be a valid 2-letter code (e.g., 'LA')")
        return v_upper

    @field_validator("zip_code")
    @classmethod
    def validate_zip_code(cls, v: str) -> str:
        v_clean = v.strip()
        if not re.match(r"^\d{5}(-\d{4})?$", v_clean):
            raise ValueError("Invalid zip code format. Must be 5 digits or ZIP+4 (e.g., '70112' or '70112-1234')")
        return v_clean

class ListingResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    listing_id: int
    host_id: int
    title: str
    description: str | None
    url: str | None
    price_per_night: Decimal
    max_guests: int
    bedrooms: int
    bathrooms: int
    is_published: bool
    address: str
    city: str
    state: str
    zip_code: str

class ListingUpdateRequestDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=256, examples=["Updated Downtown Apartment"])
    description: str = Field(default=None, max_length=512, examples=["Updated description."])
    url: str = Field(default=None, max_length=512, examples=["https://images.squarespace-cdn.com/content/v1/6671cdf4eb7de91f577a464e/1760034971967-ZUG8QSHUXLKIZOEGRV14/The+Risks+of+Overpricing_+What+Owasso+Homeowners+Should+Know+1.png"])
    price_per_night: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, examples=["135.00"])
    max_guests: int = Field(..., gt=0, examples=[4])
    bedrooms: int = Field(..., gt=0, examples=[2])
    bathrooms: int = Field(..., gt=0, examples=[1])
    is_published: bool = Field(..., examples=[True])
    address: str = Field(..., min_length=1, max_length=150, examples=["100 Main Street"])
    city: str = Field(..., min_length=1, max_length=100, examples=["New Orleans"])
    state: str = Field(..., examples=["LA"])
    zip_code: str = Field(..., examples=["70112"])

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        v_upper = v.strip().upper()
        if not re.match(r"^[A-Z]{2}$", v_upper):
            raise ValueError("State must be a valid 2-letter code (e.g., 'LA')")
        return v_upper

    @field_validator("zip_code")
    @classmethod
    def validate_zip_code(cls, v: str) -> str:
        v_clean = v.strip()
        if not re.match(r"^\d{5}(-\d{4})?$", v_clean):
            raise ValueError("Invalid zip code format. Must be 5 digits or ZIP+4 (e.g., '70112')")
        return v_clean