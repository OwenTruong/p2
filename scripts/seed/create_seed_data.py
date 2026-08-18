from .seed_model import SeedListing, SeedModel, SeedUser


ADMIN = SeedModel(
    user=SeedUser(
        email="admin@gmail.com",
        password="password123",
        first_name="Admin",
        last_name="SpaceBnB",
    ),
    listings=[
        SeedListing(
            host_id=0,
            title="Modern Downtown Apartment",
            description="Modern apartment in downtown Philadelphia.",
            price_per_night="145.00",
            max_guests=4,
            bedrooms=2,
            bathrooms=1,
            is_published=True,
            address="123 Market Street",
            city="Philadelphia",
            state="PA",
            zip_code="19106",
            url=(
                "https://images.unsplash.com/"
                "photo-1522708323590-d24dbb6b0267"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
        SeedListing(
            host_id=0,
            title="Beachfront Condo",
            description="Relaxing condo just steps from the beach.",
            price_per_night="220.00",
            max_guests=6,
            bedrooms=3,
            bathrooms=2,
            is_published=True,
            address="456 Ocean Ave",
            city="Ocean City",
            state="NJ",
            zip_code="08226",
            url=(
                "https://images.unsplash.com/"
                "photo-1499793983690-e29da59ef1c2"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
    ],
    reservations=[],
)


JOHN = SeedModel(
    user=SeedUser(
        email="john@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
    ),
    listings=[
        SeedListing(
            host_id=0,
            title="French Quarter Loft",
            description="Historic loft near the French Quarter.",
            price_per_night="185.00",
            max_guests=4,
            bedrooms=2,
            bathrooms=1,
            is_published=True,
            address="721 Royal Street",
            city="New Orleans",
            state="LA",
            zip_code="70116",
            url=(
                "https://images.unsplash.com/"
                "photo-1502672260266-1c1ef2d93688"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
        SeedListing(
            host_id=0,
            title="Garden District Cottage",
            description="Quiet cottage near historic New Orleans homes.",
            price_per_night="165.00",
            max_guests=3,
            bedrooms=2,
            bathrooms=1,
            is_published=True,
            address="1420 Magazine Street",
            city="New Orleans",
            state="LA",
            zip_code="70130",
            url=(
                "https://images.unsplash.com/"
                "photo-1568605114967-8130f3a36994"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
        SeedListing(
            host_id=0,
            title="Mountain Cabin Getaway",
            description="Peaceful mountain cabin surrounded by hiking trails.",
            price_per_night="175.00",
            max_guests=6,
            bedrooms=3,
            bathrooms=2,
            is_published=True,
            address="42 Pine Ridge Road",
            city="Asheville",
            state="NC",
            zip_code="28801",
            url=(
                "https://images.unsplash.com/"
                "photo-1449158743715-0a90ebb6d2d8"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
    ],
    reservations=[],
)


SARAH = SeedModel(
    user=SeedUser(
        email="sarah@example.com",
        password="password123",
        first_name="Sarah",
        last_name="Miller",
    ),
    listings=[
        SeedListing(
            host_id=0,
            title="Austin Music District Studio",
            description="Cozy studio near downtown restaurants and live music.",
            price_per_night="130.00",
            max_guests=2,
            bedrooms=1,
            bathrooms=1,
            is_published=True,
            address="810 Red River Street",
            city="Austin",
            state="TX",
            zip_code="78701",
            url=(
                "https://images.unsplash.com/"
                "photo-1505693416388-ac5ce068fe85"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
        SeedListing(
            host_id=0,
            title="Spacious Austin Family Home",
            description="Large home with plenty of space for families.",
            price_per_night="275.00",
            max_guests=8,
            bedrooms=4,
            bathrooms=3,
            is_published=True,
            address="2401 South Lamar Boulevard",
            city="Austin",
            state="TX",
            zip_code="78704",
            url=(
                "https://images.unsplash.com/"
                "photo-1600585152915-d208bec867a1"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
        SeedListing(
            host_id=0,
            title="Unpublished Test Property",
            description="Listing used to test unpublished behavior.",
            price_per_night="120.00",
            max_guests=2,
            bedrooms=1,
            bathrooms=1,
            is_published=False,
            address="500 Test Avenue",
            city="Dallas",
            state="TX",
            zip_code="75201",
            url=(
                "https://images.unsplash.com/"
                "photo-1570129477492-45c003edd2be"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
    ],
    reservations=[],
)


MICHAEL = SeedModel(
    user=SeedUser(
        email="michael@example.com",
        password="password123",
        first_name="Michael",
        last_name="Chen",
    ),
    listings=[
        SeedListing(
            host_id=0,
            title="Chicago River View Apartment",
            description="High-rise apartment with views of downtown Chicago.",
            price_per_night="210.00",
            max_guests=4,
            bedrooms=2,
            bathrooms=2,
            is_published=True,
            address="350 North State Street",
            city="Chicago",
            state="IL",
            zip_code="60654",
            url=(
                "https://images.unsplash.com/"
                "photo-1545324418-cc1a3fa10c00"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
        SeedListing(
            host_id=0,
            title="Cozy Chicago Studio",
            description="Affordable studio near transit and restaurants.",
            price_per_night="95.00",
            max_guests=2,
            bedrooms=1,
            bathrooms=1,
            is_published=True,
            address="1750 West Division Street",
            city="Chicago",
            state="IL",
            zip_code="60622",
            url=(
                "https://images.unsplash.com/"
                "photo-1524758631624-e2822e304c36"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
    ],
    reservations=[],
)


EMILY = SeedModel(
    user=SeedUser(
        email="emily@example.com",
        password="password123",
        first_name="Emily",
        last_name="Nguyen",
    ),
    listings=[
        SeedListing(
            host_id=0,
            title="Miami Beach Retreat",
            description="Bright condo within walking distance of Miami Beach.",
            price_per_night="260.00",
            max_guests=5,
            bedrooms=3,
            bathrooms=2,
            is_published=True,
            address="920 Collins Avenue",
            city="Miami Beach",
            state="FL",
            zip_code="33139",
            url=(
                "https://images.unsplash.com/"
                "photo-1600607687939-ce8a6c25118c"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
        SeedListing(
            host_id=0,
            title="Downtown Miami Apartment",
            description="Modern apartment overlooking downtown Miami.",
            price_per_night="195.00",
            max_guests=4,
            bedrooms=2,
            bathrooms=2,
            is_published=True,
            address="1100 Brickell Avenue",
            city="Miami",
            state="FL",
            zip_code="33131",
            url=(
                "https://images.unsplash.com/"
                "photo-1600566753190-17f0baa2a6c3"
                "?auto=format&fit=crop&w=800&q=80"
            ),
        ),
    ],
    reservations=[],
)


DAVID = SeedModel(
    user=SeedUser(
        email="david@example.com",
        password="password123",
        first_name="David",
        last_name="Wilson",
    ),
    listings=[],
    reservations=[],
)


SEED_DATA = [
    ADMIN,
    JOHN,
    SARAH,
    MICHAEL,
    EMILY,
    DAVID,
]