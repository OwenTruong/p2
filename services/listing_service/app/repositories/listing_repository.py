from app.models.listing import Listing
from app.core.config import get_config
from shared.repositories.db_repository import DBRepository

class ListingRepository(DBRepository):
    def __init__(self):
        table_name = 'listings'
        config = get_config()
        super().__init__(table_name, config)

    def save(self, listing: Listing) -> Listing:
        query = f"""
            INSERT INTO {self._table_name} (
                host_id, title, description, price_per_night, 
                max_guests, bedrooms, bathrooms, is_published, 
                address, city, state, zip_code
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING *;
        """
        return self._execute_fetch_one(
            query, 
            Listing, 
            values=[
                listing.host_id, listing.title, listing.description, listing.price_per_night,
                listing.max_guests, listing.bedrooms, listing.bathrooms, listing.is_published,
                listing.address, listing.city, listing.state, listing.zip_code
            ]
        )

    def find_all_by_host_id(self, host_id: int) -> list[Listing]:
        query = f"""
            SELECT *
            FROM {self._table_name}
            WHERE host_id=%s
            ORDER BY listing_id;
        """
        return self._execute_fetch_all(
            query,
            Listing,
            values=[host_id],
        )