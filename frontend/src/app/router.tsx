import {
    createBrowserRouter
} from "react-router-dom";

import HomePage from "../features/home/pages/HomePage";
import MyListingsPage from "../features/listings/pages/MyListingsPage";

function CreateListingPage() {
    return <h1>Create Listing (Coming Soon)</h1>;
}

function ListingDetailsPage() {
    return <h1>Listing Details (Coming Soon)</h1>;
}

export const router = createBrowserRouter([
    {
        path: "/",
        element: <HomePage />
    },
    {
        path: "/my-listings",
        element: <MyListingsPage />
    },
    {
        path: "/my-listings/create",
        element: <CreateListingPage />
    },
    {
        path: "/my-listings/:listingId",
        element: <ListingDetailsPage />
    }
]);