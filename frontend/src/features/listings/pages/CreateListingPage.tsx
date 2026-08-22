import { createListing } from "../api/listings";
import ListingForm from "../components/ListingForm";
import type { ListingFormData } from "../types";

export function CreateListingPage() {
  async function handleCreate(data: ListingFormData) {
    await createListing(data);
  }

  return (
    <ListingForm
      onSubmit={handleCreate}
      submitLabel="Create Listing"
    />
  );
}