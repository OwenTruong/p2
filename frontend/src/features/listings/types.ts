export interface Listing {
  listing_id: number;
  host_id: number;
  title: string;
  description: string;
  url: string;
  price_per_night: string;
  max_guests: number;
  beds: number;
  bathrooms: number;
  is_published: boolean;
  address: string;
  city: string;
  state: string;
  zip_code: string;
}
