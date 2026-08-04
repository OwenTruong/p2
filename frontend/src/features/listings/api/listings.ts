import type { Listing } from "../types";

const mockListings: Listing[] = [
  {
    listing_id: 1,
    host_id: 100,
    title: "Modern Apartment",
    description: "Modern apartment in downtown Philadelphia.",
    price_per_night: "145.00",
    max_guests: 4,
    beds: 2,
    bathrooms: 1,
    is_published: true,
    address: "123 Market Street",
    city: "Philadelphia",
    state: "PA",
    zip_code: "19106",
  },
  {
    listing_id: 2,
    host_id: 100,
    title: "Beach Condo",
    description: "Relaxing condo near the beach.",
    price_per_night: "220.00",
    max_guests: 6,
    beds: 3,
    bathrooms: 2,
    is_published: false,
    address: "456 Ocean Ave",
    city: "Ocean City",
    state: "NJ",
    zip_code: "08226",
  },
];

export async function getMyListings(): Promise<Listing[]> {
  // Simulate a network request
  await new Promise((resolve) => setTimeout(resolve, 700));

  return mockListings;
}