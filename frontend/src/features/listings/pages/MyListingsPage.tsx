import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import styles from "./MyListingsPage.module.css";

import { getMyListings } from "../api/listings";
import type { Listing } from "../types";
import ListingGrid from "../components/ListingGrid";
// import { ListingError } from "../errors/ListingError";

export default function MyListingsPage() {
  // React Router navigation
  const navigate = useNavigate();

  // Store the current user's listings
  const [listings, setListings] = useState<Listing[]>([]);

  // Track loading state while fetching data
  const [loading, setLoading] = useState(true);

  // Store any error message if the request fails
  const [error, setError] = useState("");
  // const [deleteError, setDeleteError] = useState<string[] | null>(null);

  // Fetch the current user's listings when the page loads
  useEffect(() => {
    async function loadListings() {
      try {
        const data = await getMyListings();
        setListings(data);
      } catch {
        setError("Failed to load listings.");
      } finally {
        setLoading(false);
      }
    }

    loadListings();
  }, []);

  // async function onDelete(id: number): Promise<void> {
  //   setDeleteError(null);

  //   try {
  //     await deleteListing(id);

  //     setListings((prev) =>
  //       prev.filter((listing) => listing.listing_id !== id)
  //     );
  //   } catch (error) {
  //     setDeleteError(
  //       error instanceof ListingError
  //         ? error.errors.map((err) => err.message)
  //         : ["Unable to delete listing. Please try again later."]
  //     );
  //   }
  // }

  // Show a loading message while data is being fetched
  if (loading) {
    return <p>Loading listings...</p>;
  }

  // Show an error message if the request failed
  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>My Listings</h1>

        {/* Navigate to the create listing page */}
        <button
          className={styles.createButton}
          onClick={() => navigate("/my-listings/create")}
        >
          Create Listing
        </button>
      </div>

      {/* {deleteError && (
        <div className={styles.alert} role="alert">
          <ul>
            {deleteError.map((error, i) => (
              <li key={i}>{error}</li>
            ))}
          </ul>
        </div>
      )} */}

      {listings.length === 0 
      ? 
        <>
          <p>You do not have any listings yet.</p>
        </> 
      :
        <ListingGrid
          listings={listings}
          getLink={(listing) => `/my-listings/${listing.listing_id}`}
          // onDelete={onDelete} 
          />
      }
    </div>
  );
}
