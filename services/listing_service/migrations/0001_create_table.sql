-- Create listings table and related enum
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'listing_status') THEN
    CREATE TYPE listing_status AS ENUM ('Available', 'Unavailable');
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS listings (
  listing_id BIGSERIAL PRIMARY KEY,
  host_id BIGINT NOT NULL REFERENCES users(user_id),
  title VARCHAR(128) NOT NULL,
  description VARCHAR(1024) NOT NULL,
  location VARCHAR(256) NOT NULL,
  price_per_night NUMERIC(10, 2) NOT NULL,
  max_guests INT NOT NULL,
  bedrooms INT NOT NULL,
  bathrooms INT NOT NULL,
  status listing_status NOT NULL DEFAULT 'Available'
);