import styles from "./ListingCard.module.css";

import type { Listing } from "../types";
import { Link } from "react-router-dom";

interface ListingCardProps {
  listing: Listing;
  linkNav: string;
}

export default function ListingCard({ listing, linkNav }: ListingCardProps) {
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

      {/* Publication status */}
      <span
        className={`${styles.status} ${
          listing.is_published ? styles.published : styles.unpublished
        }`}
      >
        {listing.is_published ? "Published" : "Unpublished"}
      </span>
    </Link>
  );
}
