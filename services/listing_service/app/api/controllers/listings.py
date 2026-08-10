from fastapi import APIRouter, Depends, status, Query
from app.dtos.listing import ListingCreateRequestDTO, ListingResponseDTO
from app.services.listing_service import ListingService
from shared.dependencies.auth import get_current_user
from shared.dtos.auth_user import AuthenticatedUser
from app.models.listingFilter import FilterParams

router = APIRouter(prefix="/api/listings", tags=["Listings"])
listing_service = ListingService()

@router.post("", response_model=ListingResponseDTO, status_code=status.HTTP_201_CREATED)
def create_listing(
    dto: ListingCreateRequestDTO,
    # current_user: AuthenticatedUser = Depends(get_current_user)
):
    created_listing = listing_service.create_listing(
        host_id=1, 
        dto=dto
    )
    
    return ListingResponseDTO.model_validate(created_listing)

@router.get("", status_code=status.HTTP_200_OK)
def get_listings(
    params: FilterParams = Query()
):
    mock_listings = [
    {
        "listing_id": 1,
        "host_id": 101,
        "title": "Cozy Downtown Apartment",
        "description": "A charming one-bedroom apartment steps from the city's best restaurants and nightlife.",
        "location": "New York, NY",
        "price_per_night": 120.00,
        "max_guests": 4,
        "bedrooms": 2,
        "bathrooms": 1,
        "status": "Available",
    },
    {
        "listing_id": 2,
        "host_id": 101,
        "title": "Sunny Beachfront Condo",
        "description": "Wake up to ocean views in this bright, modern condo just steps from the sand.",
        "location": "Miami, FL",
        "price_per_night": 250.00,
        "max_guests": 6,
        "bedrooms": 3,
        "bathrooms": 2,
        "status": "Available",
    },
    {
        "listing_id": 3,
        "host_id": 102,
        "title": "Historic French Quarter Loft",
        "description": "Exposed brick and wrought-iron balconies in the heart of New Orleans' most iconic neighborhood.",
        "location": "New Orleans, LA",
        "price_per_night": 175.00,
        "max_guests": 3,
        "bedrooms": 1,
        "bathrooms": 1,
        "status": "Unavailable",
    },
    {
        "listing_id": 4,
        "host_id": 103,
        "title": "Mountain Cabin Retreat",
        "description": "A secluded cabin surrounded by pine forest, perfect for a quiet weekend getaway.",
        "location": "Aspen, CO",
        "price_per_night": 320.00,
        "max_guests": 8,
        "bedrooms": 4,
        "bathrooms": 3,
        "status": "Available",
    },
    {
        "listing_id": 5,
        "host_id": 104,
        "title": "Minimalist Studio Near Tech Hub",
        "description": "A sleek, compact studio ideal for solo travelers or business trips.",
        "location": "San Francisco, CA",
        "price_per_night": 95.00,
        "max_guests": 2,
        "bedrooms": 0,
        "bathrooms": 1,
        "status": "Available",
    }
]

    results = mock_listings

    if params.max_price is not None:
        results = [l for l in results if l["price_per_night"] <= params.max_price]

    if params.min_beds:
        results = [l for l in results if l["bedrooms"] >= params.min_beds]

    if params.min_bathrooms:
        results = [l for l in results if l["bathrooms"] >= params.min_bathrooms]

    if params.city is not None:
        results = [l for l in results if params.city.lower() in l["location"].lower()]

    if params.state is not None:
        results = [l for l in results if params.state.lower() in l["location"].lower()]

    if params.guests > 1:
        results = [l for l in results if l["max_guests"] >= params.guests]

    # Availability filter — only listings marked "Available" are bookable
    results = [l for l in results if l["status"] == "Available"]

    return results