import { useAuth } from "@/features/auth/AuthContext";
import { Navigate, Outlet } from "react-router-dom";

export default function ProtectedRoute() {
  const { userAuth } = useAuth();

  const currentUser = userAuth.currentUser;
  const status = userAuth.status;
  
  if (status === "loading") {
    return <div>Loading...</div>;
  }

  if (status === "unauthenticated" || !currentUser) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}