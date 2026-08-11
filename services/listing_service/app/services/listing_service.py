from app.repositories.listing_repository import ListingRepository
from app.dtos.listing import ListingCreateRequestDTO
from app.models.listing import Listing
from shared.utils.exceptions import NoFetchedResultException, ActiveReservationException, UserDoesNotOwnException

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

    def delete_listing(self, host_id: int, listing_id: int) -> Listing | None:
        """
        Raises:
            - UserDoesNotOwnException
            - ActiveReservationException
            - NoFetchedResultException
        """
        if listing := self.listing_repo.find_by_id(listing_id):
            if listing.host_id != host_id:
                raise UserDoesNotOwnException()

            if listing.is_published == False: return

            # TODO: listing can not be removed because of an active reservation
            has_active_reservation = False
            if has_active_reservation:
                raise ActiveReservationException()

            listing.is_published = False
            result = self.listing_repo.save(listing)
            return result
        else:
            raise NoFetchedResultException()
        
    def get_all_by_host_id(self, host_id: int) -> list[Listing]:
        return self.listing_repo.find_all_by_host_id(host_id)
