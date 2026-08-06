import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useAuth } from '@/features/auth/AuthContext';

import styles from './Auth.module.css';

// import { logger } from '@/utils/utils';
import type { RegisterDTO } from '../types/RegisterDTO';

// const registerLogger = logger.ns('page', 'Register').seal();

export default function Page() {
  const { userAuth, register } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const pending = useRef(false);

  useEffect(() => {
    if (!pending.current) return;

    if (userAuth.status === 'authenticated') {
      pending.current = false;
      setSubmitting(false);
      navigate('/', { replace: true });
    } else if (userAuth.status === 'unauthenticated') {
      pending.current = false;
      setSubmitting(false);
      setFormError(
        userAuth.error?.message ??
          'Unable to create account. Please try again.',
      );
    }
  }, [userAuth, navigate]);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (submitting) return;

    if (password !== confirmPassword) {
      setFormError('The two passwords do not match.');
      return;
    }

    setFormError(null);
    setSubmitting(true);
    pending.current = true;

    const registerDTO: RegisterDTO = {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
    };

    await register(registerDTO);
    navigate('/login', { replace: true });
  }

  const mismatch = confirmPassword.length > 0 && password !== confirmPassword;

  return (
    <main className={styles.page}>
      <section className={styles.panel}>
        <div className={styles.header}>
          <h2 className={styles.title}>Create account</h2>
          <p className={styles.lede}>
            One account to list a space of your own or book someone
            else&rsquo;s.
          </p>
        </div>

        <form className={styles.form} onSubmit={handleSubmit} noValidate>
          {formError && (
            <p className={styles.alert} role="alert">
              {formError}
            </p>
          )}

          <div className={styles.field}>
            <label className={styles.label} htmlFor="first-name">
              First name
            </label>
            <input
              className={styles.input}
              id="first-name"
              name="firstName"
              type="text"
              autoComplete="given-name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="last-name">
              Last name
            </label>
            <input
              className={styles.input}
              id="last-name"
              name="lastName"
              type="text"
              autoComplete="family-name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="email">
              Email
            </label>
            <input
              className={styles.input}
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="password">
              Password
            </label>
            <input
              className={styles.input}
              id="password"
              name="password"
              type="password"
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="confirm-password">
              Confirm password
            </label>
            <input
              className={styles.input}
              id="confirm-password"
              name="confirmPassword"
              type="password"
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              aria-invalid={mismatch || undefined}
              aria-describedby={mismatch ? 'password-mismatch' : undefined}
              required
            />
            {mismatch && (
              <p className={styles.fieldError} id="password-mismatch">
                The two passwords do not match.
              </p>
            )}
          </div>

          <div className={styles.actions}>
            <button
              className={styles.submit}
              type="submit"
              disabled={submitting || mismatch}
            >
              {submitting ? 'Creating account…' : 'Create account'}
            </button>
          </div>
        </form>

        <div className={styles.footer}>
          <Link className={styles.altLink} to="/login">
            Already have an account?
          </Link>
        </div>
      </section>
    </main>
  );
}
