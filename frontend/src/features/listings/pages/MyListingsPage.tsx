import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import styles from "./MyListingsPage.module.css";

import { getMyListings } from "../api/listings";
import ListingCard from "../components/ListingCard";
import type { Listing } from "../types";

export default function MyListingsPage() {
    // React Router navigation
    const navigate = useNavigate();

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

    // Show a loading message while data is being fetched
    if (loading) {
        return <p>Loading listings...</p>;
    }

    // Show an error message if the request failed
    if (error) {
        return <p>{error}</p>;
    }

    // Show a message if the user has no listings
    if (listings.length === 0) {
        return <p>You don't have any listings yet.</p>;
    }

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1 className={styles.title}>
                    My Listings
                </h1>

                {/* Navigate to the create listing page */}
                <button
                    className={styles.createButton}
                    onClick={() => navigate("/my-listings/create")}
                >
                    Create Listing
                </button>
            </div>

            <div className={styles.listingsGrid}>
                {/* Render a card for each listing */}
                {listings.map((listing) => (
                    <ListingCard
                        key={listing.listing_id}
                        listing={listing}
                        onClick={() =>
                            navigate(`/my-listings/${listing.listing_id}`)
                        }
                    />
                ))}
            </div>
        </div>
    );
}