
import httpx

from app.core.config import get_config


class ListingClient:
    def __init__(self):
        config = get_config()
        self._base_url = config.listing_service_url

    def find_by_id(self, listing_id: int) -> dict | None:
        url = f"{self._base_url}/api/listings/{listing_id}"

        response = httpx.get(
            url,
            timeout=5.0,
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return response.json()