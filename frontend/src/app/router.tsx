import AccountPage from "../features/account/pages/AccountPage";
import { createBrowserRouter } from "react-router-dom";

import HomePage from "../features/home/pages/HomePage";
import MyListingsPage from "../features/listings/pages/MyListingsPage";
import AppLayout from "../layouts/AppLayout";

function CreateListingPage() {
  return <h1>Create Listing (Coming Soon)</h1>;
}

function ListingDetailsPage() {
  return <h1>Listing Details (Coming Soon)</h1>;
}

export const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/account",
        element: <AccountPage />,
      },
      {
        path: "/my-listings",
        element: <MyListingsPage />,
      },
      {
        path: "/my-listings/create",
        element: <CreateListingPage />,
      },
      {
        path: "/my-listings/:listingId",
        element: <ListingDetailsPage />,
      },
      {
        path: "/reservations",
        element: <h1>My Reservations (Coming Soon)</h1>,
      },
      {
        path: "/settings",
        element: <h1>My Profile (Coming Soon)</h1>,
      },
      {
        path: "/login",
        element: <h1>Login (Coming Soon)</h1>,
      },
      {
        path: "/logout",
        element: <h1>Logout (Coming Soon)</h1>,
      },
    ],
  },
]);