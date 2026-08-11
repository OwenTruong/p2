from pydantic import BaseModel, Field
from typing import Literal, Optional

class FilterParams(BaseModel):
    max_price: Optional[float] = Field(default=None, gt=0, examples=[200.00])
    min_beds: int = Field(default=0, ge=0, examples=[2])
    min_bathrooms: int = Field(default=0, ge=0, examples=[2])
    city: Optional[str] = Field(default=None, min_length=1, max_length=128, examples=["New Orleans"])
    state: Optional[str] = Field(default=None, min_length=1, max_length=64, examples=["LA"])
    check_in_date: Optional[str] = Field(default=None, examples=["2026-08-10"])
    check_out_date: Optional[str] = Field(default=None, examples=["2026-08-19"])
    guests: int = Field(default=1, ge=1, examples=[3])