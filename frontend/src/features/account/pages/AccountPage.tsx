import styles from "./AccountPage.module.css";

function AccountPage() {
  return (
    <main className={styles.page}>
      <section className={styles.accountCard}>
        <div className={styles.header}>
          <div className={styles.avatar}>SJ</div>

          <div>
            <h1>My Account</h1>
            <p>View and manage your account information.</p>
          </div>
        </div>

        <div className={styles.accountDetails}>
          <div className={styles.field}>
            <span className={styles.label}>First name</span>
            <span className={styles.value}>Sudiptha</span>
          </div>

          <div className={styles.field}>
            <span className={styles.label}>Last name</span>
            <span className={styles.value}>Janardhana</span>
          </div>

          <div className={styles.field}>
            <span className={styles.label}>Email</span>
            <span className={styles.value}>sudiptha@example.com</span>
          </div>
        </div>
      </section>
    </main>
  );
}

export default AccountPage;
