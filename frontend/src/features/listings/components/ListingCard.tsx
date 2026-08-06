import styles from "./ListingCard.module.css";

import type { Listing } from "../types";
import placeholderImage from "../../../assets/house-ex.jpeg";

interface ListingCardProps {
  listing: Listing;
  onClick?: () => void;
}

export default function ListingCard({ listing, onClick }: ListingCardProps) {
  return (
    <div className={styles.card} onClick={onClick}>
      {/* Placeholder image */}
      <img
        className={styles.image}
        src={placeholderImage}
        alt="Listing placeholder"
      />

      {/* Listing title */}
      <h2 className={styles.title}>{listing.title}</h2>

      {/* Property location */}
      <p className={styles.location}>
        {listing.city}, {listing.state}
      </p>

      {/* Nightly price */}
      <p className={styles.price}>${listing.price_per_night} / night</p>

      {/* Publication status */}
      <span
        className={`${styles.status} ${
          listing.is_published ? styles.published : styles.unpublished
        }`}
      >
        {listing.is_published ? "Published" : "Unpublished"}
      </span>
    </div>
  );
}
