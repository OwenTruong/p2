
-- Create reservations table and related enum

DO $$
BEGIN
  IF NOT EXISTS (Select 1 FROM pg_type WHERE typname = 'reservation_status') THEN
    CREATE TYPE reservation_status as ENUM ('Accepted', 'Cancelled');
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS reservations (
    reservation_id BIGSERIAL PRIMARY KEY,
    listing_id BIGINT NOT NULL,
    guest_id BIGINT NOT NULL,

    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    
    total_price NUMERIC(10, 2) NOT NULL
        CHECK (total_price >= 0),
    
    status reservation_status NOT NULL DEFAULT 'Accepted'
);