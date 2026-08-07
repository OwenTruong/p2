import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useAuth } from '@/features/auth/AuthContext';

import styles from './Auth.module.css';

// import { logger } from '@/utils/utils';
import type { LoginDTO } from '../types/LoginDTO';

// const loginLogger = logger.ns('page', 'Login').seal();

export default function Page() {
  const { userAuth, login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
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
        userAuth.error?.message ?? 'Unable to sign in. Please try again.',
      );
    }
  }, [userAuth, navigate]);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (submitting) return;

    setFormError(null);
    setSubmitting(true);
    pending.current = true;

    const loginDTO: LoginDTO = {
      email,
      password,
    };

    await login(loginDTO);
  }

  return (
    <main className={styles.page}>
      <section className={styles.panel}>
        <div className={styles.header}>
          <h2 className={styles.title}>Sign in</h2>
          <p className={styles.lede}>
            Pick up where you left off with your listings and reservations.
          </p>
        </div>

        <form className={styles.form} onSubmit={handleSubmit} noValidate>
          {formError && (
            <p className={styles.alert} role="alert">
              {formError}
            </p>
          )}

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
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className={styles.actions}>
            <button
              className={styles.submit}
              type="submit"
              disabled={submitting}
            >
              {submitting ? 'Signing in…' : 'Sign in'}
            </button>
          </div>
        </form>

        <div className={styles.footer}>
          <Link className={styles.altLink} to="/register">
            Create a new account today
          </Link>
        </div>
      </section>
    </main>
  );
}
