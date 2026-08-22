export interface Listing {
  listing_id: number;
  host_id: number;
  title: string;
  description: string;
  url: string;
  price_per_night: number;
  max_guests: number;
  bedrooms: number;
  bathrooms: number;
  is_published: boolean;
  address: string;
  city: string;
  state: string;
  zip_code: string;
}

export interface ListingQuery {
  max_price?: number;
  min_beds?: number;
  min_bathrooms?: number;
  city?: string;
  state?: string;
  check_in_date?: string;
  check_out_date?: string;
  guests?: number;
}

export interface ListingFormData {
  title: string;
  description: string;
  price_per_night: number;
  url: string;
  max_guests: number;
  bedrooms: number;
  bathrooms: number;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  is_published: boolean;
}