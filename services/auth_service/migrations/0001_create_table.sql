-- Create users table and related enum
DO $$
BEGIN
  IF NOT EXISTS (Select 1 FROM pg_type WHERE typname = 'user_status') THEN
    CREATE TYPE user_status as ENUM ('Active', 'Inactive');
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS users (
  user_id BIGSERIAL PRIMARY KEY,
  email VARCHAR(128) NOT NULL UNIQUE,
  password_hash VARCHAR(128) NOT NULL,
  first_name VARCHAR(64) NOT NULL,
  last_name VARCHAR(64) NOT NULL,
  status user_status NOT NULL DEFAULT 'Active'
);