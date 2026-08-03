import {
    createBrowserRouter
} from "react-router-dom";
import HomePage from "../features/home/pages/HomePage";
import MyListingsPage from "../features/listings/pages/MyListingsPage";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <HomePage />
    },
    {
        path: "/my-listings",
        element: <MyListingsPage />
    }
]);