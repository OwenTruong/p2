import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useAuth } from '@/features/auth/AuthContext';

import styles from './Auth.module.css';

// import { logger } from '@/utils/utils';
import type { LoginDTO } from '../types/LoginDTO';
import { LoginError } from '../errors/LoginError';
import { isDev } from '@/utils/utils';
// import { email } from 'zod';

// const loginLogger = logger.ns('page', 'Login').seal();
type FieldErrors = {
  email?: string;
  password?: string;
};

export default function Page() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formErrors, setFormErrors] = useState<string[] | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});

  async function handleSubmit(e: React.FormEvent) {
      e.preventDefault();

      if (submitting) return;

      const loginDTO: LoginDTO = {
        email,
        password
      }

      const validationErrors = validateLogin(loginDTO);

      if (Object.keys(validationErrors).length > 0) {
        setFieldErrors(validationErrors);
        return;
      }

      setFieldErrors({});
      setFormErrors(null);
      setSubmitting(true);

      try {
          await login(loginDTO);

          navigate('/', { replace: true });
      } catch(error) {

          if (error instanceof LoginError) {
            const errorMessages: string[] = error.errors.map(e => e.message);
            setFormErrors(errorMessages ?? ["Unable to sign in."]);
          } else {
            setFormErrors([
                'Unable to sign in. Please try again.',
            ]);
          }

      } finally {
          setSubmitting(false);
      }
  }

  async function handleAdminLogin() {
    try {
      await login({
        email: "admin@gmail.com",
        password: "password123"
      });
      navigate('/', { replace: true });

    } catch(error) {

      if (error instanceof LoginError) {
        const errorMessages: string[] = error.errors.map(e => e.message);
        setFormErrors(errorMessages ?? ["Unable to sign in."]);
      } else {
        setFormErrors([
            'Unable to sign in. Please try again.',
        ]);
      }

    } finally {
        setSubmitting(false);
    }
  }

  return (
    <main className={styles.page}>
      <section className={styles.panel}>

        {/* DEV ONLY */}
        {isDev && (
          <div className={styles.devTools}>
            <span className={styles.devLabel}>Development</span>
            <button
              className={styles.adminLogin}
              type="button"
              disabled={submitting}
              onClick={handleAdminLogin}
            >
              Login as Admin
            </button>
          </div>
        )}

        <div className={styles.header}>
          <h2 className={styles.title}>Sign in</h2>
          <p className={styles.lede}>
            Pick up where you left off with your listings and reservations.
          </p>
        </div>

        <form className={styles.form} onSubmit={handleSubmit} noValidate>
          {formErrors && (
            <p className={styles.alert} role="alert">
              {formErrors}
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
              aria-invalid={!!fieldErrors.email || undefined}
              aria-describedby={fieldErrors.email ? 'email-error' : undefined}
              required
            />

            {fieldErrors.email && (
              <p className={styles.fieldError} id="email-error">
                {fieldErrors.email}
              </p>
            )}
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
              minLength={8}
              maxLength={128}
              aria-invalid={!!fieldErrors.password || undefined}
              aria-describedby={fieldErrors.password ? 'password-error' : undefined}
              required
            />

            {fieldErrors.password && (
              <p className={styles.fieldError} id="password-error">
                {fieldErrors.password}
              </p>
            )}
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

function validateLogin(input : LoginDTO): FieldErrors {

  const errors: FieldErrors = {};
  const email = input.email;
  const password = input.password;

  if (!email) {
    errors.email = 'Email is required.';
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.email = 'Enter a valid email address.';
  }

  if (password.length < 8) {
    errors.password = 'Password must be at least 8 characters.';
  } else if (password.length > 128) {
    errors.password = 'Password must be at most 128 characters.';
  }

  return errors;
}