import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { useUser } from '@/features/auth/userContext';

// import { logger } from '@/utils/utils';
import type { LoginDTO } from '../types/LoginDTO';

// const loginLogger = logger.ns('page', 'Login').seal();

export default function Page() {
  const { userAuth, login } = useUser();
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
    <main>
      <section>
        <h2>Login</h2>

        <form onSubmit={handleSubmit} noValidate>
          {formError && <p role="alert">{formError}</p>}

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
              autoComplete="current-password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div>
            <button type="submit" disabled={submitting}>
              {submitting ? 'Signing in…' : 'Sign in'}
            </button>
          </div>
        </form>

        <Link to="/register">Create a new account today</Link>
      </section>
    </main>
  );
}
