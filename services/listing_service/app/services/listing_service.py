from app.repositories.listing_repository import ListingRepository
from app.dtos.listing import ListingCreateRequestDTO
from app.models.listing import Listing
from shared.dtos.auth_user import AuthenticatedUser
from fastapi import HTTPException, status

class ListingService:
    def __init__(self, listing_repo: ListingRepository | None = None):
        self.listing_repo = listing_repo or ListingRepository()

    def create_listing(self, host_id: int, dto: ListingCreateRequestDTO) -> Listing:
        listing = Listing(
            host_id=host_id,  
            title=dto.title,
            description=dto.description,
            price_per_night=dto.price_per_night,
            max_guests=dto.max_guests,
            bedrooms=dto.bedrooms,
            bathrooms=dto.bathrooms,
            is_published=True, 
            address=dto.address,
            city=dto.city,
            state=dto.state,
            zip_code=dto.zip_code
        )
        return self.listing_repo.save(listing)
    
    def get_listing(self, listing_id: int, current_user: AuthenticatedUser | None = None) -> Listing:
        listing = self.listing_repo.find_by_id(listing_id)

        if listing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found",
            )
        
        # Published listings can be viewed by anyone
        if listing.is_published:
            return listing
        
        # Unpublished listings require authentication
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required to view this listing",
            )
        
        # Unpublished listings can only be viewed by owner
        if listing.host_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this listing",
            )
        
        return listing