from app.models.listing import Listing
from app.core.config import get_config
from app.models.listingFilter import FilterParams
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

    def find_all(self, params: FilterParams) -> list[Listing]:
        conditions = []
        values = []

        if params.max_price is not None:
            conditions.append("price_per_night <= %s")
            values.append(params.max_price)

        if params.min_beds:
            conditions.append("bedrooms >= %s")
            values.append(params.min_beds)

        if params.min_bathrooms:
            conditions.append("bathrooms >= %s")
            values.append(params.min_bathrooms)

        if params.city is not None:
            conditions.append("city ILIKE %s")
            values.append(params.city)

        if params.state is not None:
            conditions.append("state ILIKE %s")
            values.append(params.state)

        if params.guests > 1:
            conditions.append("max_guests >= %s")
            values.append(params.guests)

        # Only ever return published/bookable listings
        conditions.append("is_published = %s")
        values.append(True)

        where_clause = " AND ".join(conditions)

        query = f"""
            SELECT * FROM {self._table_name}
            WHERE {where_clause};
        """

        return self._execute_fetch_all(query, Listing, values=values)

