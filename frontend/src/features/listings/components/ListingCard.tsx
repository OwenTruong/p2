import styles from "./ListingCard.module.css";
// import { Trash2 } from "lucide-react";

import type { Listing } from "../types";
import { Link } from "react-router-dom";

interface ListingCardProps {
  listing: Listing;
  linkNav: string;
  // onDelete?: (id: number) => Promise<void>;
}

export default function ListingCard({ listing, linkNav }: ListingCardProps) {

  // async function handleDelete(e: React.MouseEvent<HTMLButtonElement>) {
  //   e.preventDefault();
  //   e.stopPropagation();

  //   const confirmed = window.confirm(
  //     `Delete "${listing.title}"?`
  //   );

  //   if (!confirmed) return;

  //   await onDelete?.(listing.listing_id);
  // }

  return (
    <Link 
    className={styles.card} 
    to={linkNav}>
      {/* Listing image */}
      <img
        className={styles.image}
        src={listing.url}
        alt="listing image"
      />

      {/* Listing title */}
      <h2 className={styles.title}>{listing.title}</h2>

      {/* Property location */}
      <p className={styles.location}>
        {listing.city}, {listing.state}
      </p>

      {/* Nightly price */}
      <p className={styles.price}>${listing.price_per_night} / night</p>

      {linkNav.includes("my") && 
        <>
          {/* Publication status */}
          <span
            className={`${styles.status} ${
              listing.is_published ? styles.published : styles.unpublished
            }`}
          >
            {listing.is_published ? "Published" : "Unpublished"}
          </span>

          {/* <button
            type="button"
            className={styles.deleteButton}
            onClick={handleDelete}
            aria-label={`Delete ${listing.title}`}
            title="Delete listing"
          >
            <Trash2 size={18} />
          </button> */}
        </>
      }
    </Link>
  );
}
