from app.models.listing import Listing
from app.core.config import get_config
from shared.repositories.db_repository import DBRepository
from shared.utils.exceptions import NoFetchedResultException

class ListingRepository(DBRepository):
    def __init__(self):
        table_name = 'listings'
        config = get_config()
        super().__init__(table_name, config)

    def save(self, listing: Listing) -> Listing:
        insert_query = f"""
            INSERT INTO {self._table_name} (
                host_id, title, description, price_per_night, 
                max_guests, bedrooms, bathrooms, is_published, 
                address, city, state, zip_code
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING *;
        """

        update_query = f"""
            UPDATE {self._table_name} 
            SET title = %s, description = %s, price_per_night = %s, 
                max_guests = %s, bedrooms = %s, bathrooms = %s,
                is_published = %s, address = %s, city = %s, state = %s, zip_code = %s
            WHERE listing_id=%s
            RETURNING *;
        """

        if listing.listing_id == None:
            return self._execute_fetch_one(
                insert_query,
                Listing,
                values=[
                    listing.host_id, listing.title, listing.description, listing.price_per_night,
                    listing.max_guests, listing.bedrooms, listing.bathrooms, listing.is_published,
                    listing.address, listing.city, listing.state, listing.zip_code
                ]
            )
        else:
            return self._execute_fetch_one(
                update_query,
                Listing,
                values=[
                    listing.title, listing.description, listing.price_per_night,
                    listing.max_guests, listing.bedrooms, listing.bathrooms,
                    listing.is_published, listing.address, listing.city, listing.state, listing.zip_code,
                    listing.listing_id
                ]
            )

    def find_by_id(self, id: int) -> Listing | None:
        query = f"SELECT * FROM {self._table_name} WHERE user_id=%s"

        try:
            return self._execute_fetch_one(query, Listing, values=[id])
        except NoFetchedResultException:
            return None