import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router-dom";

import AccountPage from "../../features/account/pages/AccountPage";
import HomePage from "../../features/home/pages/HomePage";
import MyListingsPage from "../../features/listings/pages/MyListingsPage";
import LoginPage from "../../features/auth/pages/LoginPage";
import RegisterPage from "../../features/auth/pages/RegisterPage";
import AppLayout from "../../layouts/AppLayout";
import ProtectedRoute from "./ProtectedRoute";
import GuestRoute from "./GuestRoute";
import ListingDetailsPage from "@/features/listings/pages/ListingDetailsPage";
import { CreateListingPage } from "@/features/listings/pages/CreateListingPage";
import { UpdateListingPage } from "@/features/listings/pages/UpdateListingPage";

export const router = createBrowserRouter(
  createRoutesFromElements(
    <Route element={<AppLayout />}>
      {/* Public */}
      <Route path="/" element={<HomePage />} />
      <Route
        path="/listings/:listingId"
        element={<ListingDetailsPage />}
      />

      {/* Guest only */}
      <Route element={<GuestRoute />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>
      
      {/* Protected */}
      <Route element={<ProtectedRoute />}>
        <Route path="/my-listings" element={<MyListingsPage />} />
        <Route
          path="/my-listings/create"
          element={<CreateListingPage />}
        />
        <Route
          path="/my-listings/:listingId"
          element={<UpdateListingPage />}
        />

        <Route
          path="/reservations"
          element={<h1>My Reservations (Coming Soon)</h1>}
        />
        
        <Route path="/settings" element={<AccountPage />} />
      </Route>
    </Route>,
  ),
);