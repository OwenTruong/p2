from fastapi import APIRouter, Depends, status, HTTPException
from app.dtos.listing import ListingCreateRequestDTO, ListingResponseDTO
from app.services.listing_service import ListingService
from shared.dependencies.auth import get_optional_current_user
from shared.dtos.auth_user import AuthenticatedUser

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

@router.get("/{listing_id}", response_model=ListingResponseDTO)
def get_listing(listing_id: int, current_user: AuthenticatedUser | None = Depends(get_optional_current_user)):
    listing = listing_service.get_listing(listing_id=listing_id, current_user=current_user)
    
    return ListingResponseDTO.model_validate(listing)