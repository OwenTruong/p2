import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useUser } from '@/features/auth/userContext';
// import styles from './Auth.module.css';

// import { logger } from '@/utils/utils';
import type { RegisterDTO } from '../types/RegisterDTO';

// const registerLogger = logger.ns('page', 'Register').seal();

export default function Page() {
  const { userAuth, register } = useUser();
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
    <main>
      <section>
        <h2>Register</h2>

        <form onSubmit={handleSubmit} noValidate>
          {formError && <p role="alert">{formError}</p>}

          <div>
            <label htmlFor="first-name">First name</label>
            <input
              id="first-name"
              name="firstName"
              type="text"
              autoComplete="given-name"
              placeholder="First name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="last-name">Last name</label>
            <input
              id="last-name"
              name="lastName"
              type="text"
              autoComplete="family-name"
              placeholder="Last name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="new-password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div>
            <label htmlFor="confirm-password">Confirm password</label>
            <input
              id="confirm-password"
              name="confirmPassword"
              type="password"
              autoComplete="new-password"
              placeholder="Confirm password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              aria-invalid={mismatch || undefined}
              aria-describedby={mismatch ? 'password-mismatch' : undefined}
              required
            />
            {mismatch && (
              <p id="password-mismatch">The two passwords do not match.</p>
            )}
          </div>

          <div>
            <button type="submit" disabled={submitting || mismatch}>
              {submitting ? 'Creating account…' : 'Create account'}
            </button>
          </div>
        </form>

        <Link to="/login">Already have an account?</Link>
      </section>
    </main>
  );
}
