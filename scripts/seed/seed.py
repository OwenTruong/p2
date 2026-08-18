import os
import httpx

from .seed_model import SeedListing, SeedUser, SeedUserResponse

from .create_seed_data import SEED_DATA
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("INTERNAL_DNS_AUTH_SERVICE_URL", "http://auth_service:8000")
LISTING_SERVICE_URL = os.getenv("INTERNAL_DNS_LISTING_SERVICE_URL", "http://listing_service:8000")
RESERVATION_SERVICE_URL = os.getenv("INTERNAL_DNS_RESERVATION_SERVICE_URL", "http://reservation_service:8000")

client = httpx.Client(
    timeout=10.0,
)

def seed_user(user : SeedUser) -> SeedUserResponse:

    try:
        response = client.post(
            f"{AUTH_SERVICE_URL}/api/auth/register",
            json=user.model_dump(mode="json")
        )
        response.raise_for_status()

        return SeedUserResponse.model_validate(response.json())
    
    except Exception as exc:
        print(f"Skipped seeding user {user.email}: {exc}")
        return None

def login(user: SeedUser) -> None:

    response = client.post(
        f"{AUTH_SERVICE_URL}/api/auth/login",
        json={
            "email": user.email,
            "password": user.password,
        },
    )

    response.raise_for_status()

    print(f"Logged in as {user.email}")

def get_access_token() -> str:
    token = client.cookies.get("access_token")

    if token is None:
        raise RuntimeError(
            "Login succeeded but no access_token cookie was returned."
        )

    return token

def seed_listings(user : SeedUserResponse, listings : list[SeedListing]) -> None:
    # Initialize listing client

    access_token = get_access_token()

    for listing in listings:
        listing.host_id = user.user_id
        try:

            print(listing)
            response = client.post(
                f"{LISTING_SERVICE_URL}/api/listings",
                json=listing.model_dump(mode="json"),
                cookies={
                    "access_token": access_token
                },
            )
        
            response.raise_for_status()

            print(f"Created listing: {listing.title}")

        except Exception as exc:
            print(f"Skipped seeding listing {listing.title}: {exc}")

def logout() -> None:
    try:
        response = client.post(
            f"{AUTH_SERVICE_URL}/api/auth/logout"
        )

        response.raise_for_status()

    finally:
        client.cookies.clear()


if __name__ == "__main__":
    for seed in SEED_DATA:
        registered_user = seed_user(seed.user)

        if registered_user is None:
            continue

        try:
            login(seed.user)

            seed_listings(
                registered_user,
                seed.listings,
            )

        finally:
            logout()

    client.close()