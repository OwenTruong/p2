import styles from "./AccountPage.module.css";
import { useAuth } from "@/features/auth/AuthContext";

function AccountPage() {

  const { userAuth } = useAuth();

  if (userAuth.status === "loading") {
    return <p>Loading...</p>;
  }

  if (!userAuth.currentUser) {
    return null;
  }
  
  const user = userAuth.currentUser;

  const initials = `${user.first_name[0] ?? ""}${user.last_name[0] ?? ""}`.toUpperCase();

  return (
    <main className={styles.page}>
      <section className={styles.accountCard}>
        <div className={styles.header}>
          <div className={styles.avatar}>{initials}</div>

          <div>
            <h1>My Account</h1>
            <p>View and manage your account information.</p>
          </div>
        </div>

        <div className={styles.accountDetails}>
          <div className={styles.field}>
            <span className={styles.label}>First name</span>
            <span className={styles.value}>{user.first_name}</span>
          </div>

          <div className={styles.field}>
            <span className={styles.label}>Last name</span>
            <span className={styles.value}>{user.last_name}</span>
          </div>

          <div className={styles.field}>
            <span className={styles.label}>Email</span>
            <span className={styles.value}>{user.email}</span>
          </div>
        </div>
      </section>
    </main>
  );
}

export default AccountPage;
