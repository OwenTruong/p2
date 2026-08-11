import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useAuth } from '@/features/auth/AuthContext';

import styles from './Auth.module.css';

// import { logger } from '@/utils/utils';
import type { RegisterDTO } from '../types/RegisterDTO';
import { RegistrationError } from '../errors/RegistrationError';

// const registerLogger = logger.ns('page', 'Register').seal();
type FieldErrors = {
  first_name?: string;
  last_name?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
};

export default function Page() {
  const { userAuth, register } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [formError, setFormError] = useState<string[] | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  
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
      setFormError(['Registration failed. Please check your input and try again.']);
    }
  }, [userAuth, navigate]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (submitting) return;

    const errors = validateRegistration({
      firstName,
      lastName,
      email,
      password,
      confirmPassword,
    });

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }

    setFieldErrors({});
    setFormError(null);
    setSubmitting(true);

    const registerDTO: RegisterDTO = {
      first_name: firstName.trim(),
      last_name: lastName.trim(),
      email: email.trim().toLowerCase(),
      password,
    };

<<<<<<< HEAD
    await register(registerDTO);
    if (userAuth.error != null) navigate('/login', { replace: true });
=======
    try {
      await register(registerDTO);
      navigate('/login', { replace: true });
    } catch (error) {
      setFormError(
        error instanceof RegistrationError
          ? error.errors.map((err) => err.message)
          : ['An unexpected error occurred. Please try again later.']
      );
    } finally {
      setSubmitting(false);
    }
>>>>>>> origin/master
  }

  // const mismatch = confirmPassword.length > 0 && password !== confirmPassword;

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
              <ul>
                {formError.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
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
              minLength={2}
              maxLength={64}
              aria-invalid={!!fieldErrors.first_name || undefined}
              aria-describedby={fieldErrors.first_name ? 'first-name-error' : undefined}
              required
            />

            {fieldErrors.first_name && (
              <p className={styles.fieldError} id="first-name-error">
                {fieldErrors.first_name}
              </p>
            )}
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
              minLength={2}
              maxLength={64}
              aria-invalid={!!fieldErrors.last_name || undefined}
              aria-describedby={fieldErrors.last_name ? 'last-name-error' : undefined}
              required
            />

            {fieldErrors.last_name && (
              <p className={styles.fieldError} id="last-name-error">
                {fieldErrors.last_name}
              </p>
            )}
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
              minLength={8}
              maxLength={128}
              aria-invalid={!!fieldErrors.confirmPassword || undefined}
              aria-describedby={
                fieldErrors.confirmPassword ? 'confirm-password-error' : undefined
              }
              required
            />

            {fieldErrors.confirmPassword && (
              <p className={styles.fieldError} id="confirm-password-error">
                {fieldErrors.confirmPassword}
              </p>
            )}
          </div>

          <div className={styles.actions}>
            <button
              className={styles.submit}
              type="submit"
              // disabled={submitting || mismatch}
              disabled={submitting}
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


function validateRegistration(input: {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
}): FieldErrors {
  const errors: FieldErrors = {};

  const firstName = input.firstName.trim();
  const lastName = input.lastName.trim();
  const email = input.email.trim().toLowerCase();

  if (firstName.length < 2) {
    errors.first_name = 'First name must be at least 2 characters.';
  } else if (firstName.length > 64) {
    errors.first_name = 'First name must be less than 64 characters.';
  } else if (![...firstName].some((char) => /\p{L}/u.test(char))) {
    errors.first_name = 'First name must contain at least one letter.';
  }

  if (lastName.length < 2) {
    errors.last_name = 'Last name must be at least 2 characters.';
  } else if (lastName.length > 64) {
    errors.last_name = 'Last name must be less than 64 characters.';
  } else if (![...lastName].some((char) => /\p{L}/u.test(char))) {
    errors.last_name = 'Last name must contain at least one letter.';
  }

  if (!email) {
    errors.email = 'Email is required.';
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.email = 'Enter a valid email address.';
  }

  if (input.password.length < 8) {
    errors.password = 'Password must be at least 8 characters.';
  } else if (input.password.length > 128) {
    errors.password = 'Password must be at most 128 characters.';
  }

  if (input.password !== input.confirmPassword) {
    errors.confirmPassword = 'The two passwords do not match.';
  }

  return errors;
}
