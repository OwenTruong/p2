import { useParams } from "react-router-dom";
import styles from "./ListingDetailsPage.module.css";
import { useEffect, useState } from "react";
import type { Listing } from "../types";
import { getListingDetails } from "../api/listings";

export default function ListingDetailsPage() {
    const { listingId } = useParams();

    const [listing, setListing] = useState<Listing | null>(null);
    const [loading, setLoading] = useState(true);

    const [checkIn, setCheckIn] = useState("");
    const [checkOut, setCheckOut] = useState("");
    const [guestCount, setGuestCount] = useState(1);

    useEffect(() => {
        async function loadListing() {
            try {
                const listing = await getListingDetails(Number(listingId))

                setListing(listing);
            } finally {
                setLoading(false);
            }
        }

        loadListing();
    }, [listingId]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (!listing) {
        return <p>Listing not found.</p>;
    }

    const calculateNightCount = () => {
        if (!checkIn || !checkOut) {
            return 0;
        }

        const start = new Date(checkIn);
        const end = new Date(checkOut);

        const difference = end.getTime() - start.getTime();

        return Math.max(
            0,
            Math.ceil(difference / (1000 * 60 * 60 * 24))
        );
    };

    const nightCount = calculateNightCount();

    const totalCost =
        Number(listing.price_per_night) * nightCount;

    return (
        <main className={styles.page}>
            <section className={styles.header}>
                <h1>{listing.title}</h1>
                <p>
                    {listing.city}, {listing.state}
                </p>
            </section>

            <section className={styles.imageSection}>
                <img
                    className={styles.imagePlaceholder}
                    src={listing.url}
                    alt={listing.title}
                />
            </section>

            <div className={styles.contentGrid}>
                <section className={styles.listingInfo}>
                    <div className={styles.hostSection}>
                        <h2>Hosted by ...</h2>

                        <div className={styles.features}>
                            <span>{listing.max_guests} guests</span>
                            <span>{listing.bedrooms} beds</span>
                            <span>{listing.bathrooms} bathrooms</span>
                        </div>
                    </div>

                    <div className={styles.descriptionSection}>
                        <h2>About this listing</h2>
                        <p>{listing.description}</p>
                    </div>

                    <div className={styles.locationSection}>
                        <h2>Location</h2>
                        <p>
                            {listing.address}, {listing.city},{" "}
                            {listing.state}
                        </p>
                    </div>
                </section>

                <aside>
                    <div className={styles.reservationCard}>
                        <div className={styles.price}>
                            <span className={styles.priceAmount}>
                                ${listing.price_per_night}
                            </span>

                            <span className={styles.priceUnit}>
                                {" "}
                                / night
                            </span>
                        </div>

                        <div className={styles.dateFields}>
                            <div className={styles.dateField}>
                                <label>CHECK-IN</label>

                                <input
                                    type="date"
                                    value={checkIn}
                                    onChange={(event) =>
                                        setCheckIn(event.target.value)
                                    }
                                />
                            </div>

                            <div className={styles.dateField}>
                                <label>CHECKOUT</label>

                                <input
                                    type="date"
                                    value={checkOut}
                                    min={checkIn}
                                    onChange={(event) =>
                                        setCheckOut(event.target.value)
                                    }
                                />
                            </div>
                        </div>

                        <div className={styles.guestField}>
                            <label>GUESTS</label>

                            <select
                                value={guestCount}
                                onChange={(event) =>
                                    setGuestCount(
                                        Number(event.target.value)
                                    )
                                }
                            >
                                {Array.from(
                                    { length: listing.max_guests },
                                    (_, index) => index + 1
                                ).map((count) => (
                                    <option key={count} value={count}>
                                        {count}{" "}
                                        {count === 1
                                            ? "guest"
                                            : "guests"}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <button
                            className={styles.reserveButton}
                            disabled={nightCount === 0}
                        >
                            Reserve
                        </button>

                        <p className={styles.chargeNotice}>
                            You won't be charged yet
                        </p>

                        {nightCount > 0 && (
                            <div className={styles.priceBreakdown}>
                                <div>
                                    <span>
                                        ${listing.price_per_night} ×{" "}
                                        {nightCount} nights
                                    </span>

                                    <span>
                                        ${totalCost.toFixed(2)}
                                    </span>
                                </div>

                                <div className={styles.total}>
                                    <span>Total</span>
                                    <span>
                                        ${totalCost.toFixed(2)}
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>
                </aside>
            </div>
        </main>
    );
}