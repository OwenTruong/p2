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
def get_listings(params: FilterParams = Query()):
    return listing_service.find_all(params)