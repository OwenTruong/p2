import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import type { Listing } from "../types";
import ListingForm from "../components/ListingForm";
import { getListingDetails, updateListing } from "../api/listings";

export function UpdateListingPage() {
  const { listingId } = useParams();
  const [listing, setListing] = useState<Listing | null>(null);

  useEffect(() => {
    async function loadListing() {
      if (!listingId) return;

      const data = await getListingDetails(Number(listingId));
      setListing(data);
    }

    loadListing();
  }, [listingId]);

  if (!listing) {
    return <p>Loading...</p>;
  }

  return (
    <ListingForm
      initialValues={listing}
      onSubmit={(data) => updateListing(Number(listingId!), data)}
      submitLabel="Update Listing"
    />
  );
}