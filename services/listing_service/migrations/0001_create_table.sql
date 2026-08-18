-- Create listings table and related enum
CREATE TABLE IF NOT EXISTS listings (
    listing_id BIGSERIAL PRIMARY KEY,
    host_id BIGINT NOT NULL,

    title VARCHAR(128) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    url VARCHAR(1024) NOT NULL,

    price_per_night NUMERIC(10, 2) NOT NULL
        CHECK (price_per_night >= 0),

    max_guests INT NOT NULL
        CHECK (max_guests > 0),

    bedrooms INT NOT NULL
        CHECK (bedrooms >= 0),

    bathrooms INT NOT NULL
        CHECK (bathrooms >= 0),

    is_published BOOLEAN NOT NULL DEFAULT FALSE,

    address VARCHAR(128) NOT NULL,
    city VARCHAR(64) NOT NULL,
    state CHAR(2) NOT NULL,
    zip_code VARCHAR(16) NOT NULL
);