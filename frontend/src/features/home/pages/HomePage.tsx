import ListingGrid from "@/features/listings/components/ListingGrid";
import styles from "./HomePage.module.css";
import { useEffect, useState } from "react";
import { getListings } from "@/features/listings/api/listings";
import type { Listing } from "@/features/listings/types";

export default function HomePage() {

  // Store the current user's listings
  const [listings, setListings] = useState<Listing[]>([]);

  // Track loading state while fetching data
  const [loading, setLoading] = useState(true);

  // Store any error message if the request fails
  const [error, setError] = useState("");

  // Fetch the current user's listings when the page loads
  useEffect(() => {
    async function loadListings() {
      try {
        const data = await getListings();
        setListings(data);
      } catch {
        setError("Failed to load listings.");
      } finally {
        setLoading(false);
      }
    }

    loadListings();
  }, []);

  // Show a loading message while data is being fetched
  if (loading) {
    return <p>Loading listings...</p>;
  }

  // Show an error message if the request failed
  if (error) {
    return <p>{error}</p>;
  }
  
  return (
    <main className={styles.home}>
      <h1>SpaceBnB</h1>

      <p>Find your next stay.</p>

      <div className={styles.searchPanel}>
        Search listings...
      </div>

      <ListingGrid
        listings={listings}
        getLink={(listing) => `/listings/${listing.listing_id}`} />

    </main>
  );
}
