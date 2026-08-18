import type { Listing } from "../types";
import ListingCard from "./ListingCard";
import styles from "./ListingGrid.module.css";

interface ListingGridProps {
  listings: Listing[];
  getLink: (listing: Listing) => string;
}

export default function ListingGrid({
  listings,
  getLink
}: ListingGridProps) {
  return (

    // Renders a card for each listing
    <div className={styles.listingsGrid}>
      {listings.map((listing) => (
        <ListingCard
          key={listing.listing_id}
          listing={listing}
          linkNav={getLink(listing)}
        />
      ))}
    </div>
  );
}