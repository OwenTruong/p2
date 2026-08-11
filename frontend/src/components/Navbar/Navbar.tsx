// src/components/Navbar/Navbar.jsx

import { NavLink, useNavigate, type NavLinkRenderProps } from 'react-router-dom';
import styles from './Navbar.module.css';
import { useAuth } from '@/features/auth/AuthContext';

export default function Navbar() {
  const navigate = useNavigate();
  const auth = useAuth();
  const getLinkClass = ({ isActive }: NavLinkRenderProps) =>
    isActive ? `${styles.link} ${styles.activeLink}` : styles.link;

  return (
    <header className={styles.header}>
      <nav className={styles.navbar}>
        <NavLink to="/" className={styles.brand}>
          SpaceBnB
        </NavLink>

        <div className={styles.links}>
          <NavLink to="/" className={getLinkClass} end>
            Home
          </NavLink>

          {/* DISPLAY ONLY FOR NON-AUTHENTICATED USERS */}
          {auth.userAuth.status != 'authenticated' && (
            <NavLink to="/login" className={getLinkClass}>
              Login
            </NavLink>
          )}

          {/* DISPLAY ONLY FOR AUTHENTICATED USERS */}
          {auth.userAuth.status === 'authenticated' && (
            <>
            {/* PROTECTED ROUTES */}
            <NavLink to="/my-listings" className={getLinkClass}>
              My Listings
            </NavLink>

            <NavLink to="/reservations" className={getLinkClass}>
              My Reservations
            </NavLink>

            <NavLink to="/settings" className={getLinkClass}>
              My Profile
            </NavLink>
            
            <button
              type="button"
              onClick={async () => {
                await auth.logout();
                navigate("/", {replace: true});
              }}
              className={`${styles.link} ${styles.logout}`}
            >
              Logout
            </button>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
