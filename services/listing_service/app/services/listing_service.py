from app.repositories.listing_repository import ListingRepository
from app.dtos.listing import ListingCreateRequestDTO
from app.models.listing import Listing

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

    def get_all_by_host_id(self, host_id: int) -> list[Listing]:
        return self.listing_repo.get_listings_by_host_id(host_id)