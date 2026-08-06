// src/components/Navbar/Navbar.jsx

import { NavLink, type NavLinkRenderProps } from "react-router-dom";
import styles from "./Navbar.module.css";

export default function Navbar() {
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

          {/* DISPLAY ONLY FOR NON-AUTHENTICATED USERS */}
          <NavLink to="/login" className={getLinkClass}>
            Login
          </NavLink>

          {/* DISPLAY ONLY FOR AUTHENTICATED USERS */}
          <NavLink to="/logout" className={getLinkClass}>
            Logout
          </NavLink>
        </div>
      </nav>
    </header>
  );
}
