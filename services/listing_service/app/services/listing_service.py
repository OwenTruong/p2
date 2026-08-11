from app.repositories.listing_repository import ListingRepository
from app.dtos.listing import ListingCreateRequestDTO
from app.models.listing import Listing
from app.models.listingFilter import FilterParams

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

    def find_all(self, query: FilterParams):
        return self.listing_repo.find_all(query)