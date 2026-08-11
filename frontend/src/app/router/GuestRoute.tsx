import { useAuth } from "@/features/auth/AuthContext";
import { Navigate, Outlet } from "react-router-dom";

export default function GuestRoute() {
  const { userAuth } = useAuth();

  const currentUser = userAuth.currentUser;
  const status = userAuth.status;
  
  if (status === "loading") {
    return <div>Loading...</div>;
  }

  if (status === "authenticated" || currentUser) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}