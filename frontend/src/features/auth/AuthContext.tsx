import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';

import { type UserAuth } from './types/UserAuth';
import { logger } from '@/utils/utils';
import { loginUser } from './api/loginUser';
import { logoutUser } from './api/logoutUser';
import { UnexpectedError } from '@/errors/UnexpectedError';
import { eventNames } from '@/utils/netquest';

import { config } from '@/utils/config';
import type { RegisterDTO } from './types/RegisterDTO';
import { registerUser } from './api/registerUser';
import type { LoginDTO } from './types/LoginDTO';
import { fetchUser } from './api/fetchUser';

const fileLogger = logger.ns('userContext').seal();
const providerLogger = fileLogger.ns('provider').seal();

const AuthContext = createContext<{
  userAuth: UserAuth;
  logout: () => Promise<void>;
  login: (loginDTO: LoginDTO) => Promise<void>;
  register: (registerDTO: RegisterDTO) => Promise<void>;
} | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {

  const [userAuth, setUserAuth] = useState<UserAuth>(() => {
    return {
      currentUser: null,
      status: 'loading'
    };
  });

  /**
   * Signs out and clears local auth state.
   *
   * Never rejects, and always clears state even if the server call fails.
   * A failed logout is logged but not bubbled up. `userAuth.error` is always null
   * afterwards.
   */
  const logout = useCallback(async () => {
    try {
      await logoutUser(config.logoutPath);
      setUserAuth({
        currentUser: null,
        status: 'unauthenticated'
      });
    } catch (err) {
      providerLogger.warn(`Unable to logout: ${err}`);
      
      // This is functionally similar to a successful logout
      setUserAuth({
        currentUser: null,
        status: 'unauthenticated'
      });
    }
  }, []);

  /**
   * Attempts to sign in and populate the current user.
   *
   * Never rejects. On failure, `userAuth.status` becomes 'unauthenticated'
   * and `userAuth.error` is set, but not until the next render, so do not
   * read `userAuth` immediately after awaiting this. React to it in a
   * useEffect keyed on `userAuth`.
   *
   * Possible values of `userAuth.error`:
   *  * UserLoginCredentialsError
   *  * UserDeactivatedError
   *  * UserNotFoundError
   *  * UnexpectedError
   */
  const login = useCallback(async (loginDTO: LoginDTO) => {
    try {
      setUserAuth({
        currentUser: null,
        status: 'loading'
      });
      await loginUser(config.loginPath, loginDTO);
      const user = await fetchUser(config.fetchUserPath);
      setUserAuth({
        currentUser: user,
        status: 'authenticated'
      });
    } catch (err) {
      providerLogger.warn(`Unable to login: ${err}`);
      setUserAuth({
        currentUser: null,
        status: 'unauthenticated'
      });

      throw err
    }
  }, []);

  /**
   * Attempts to register and populate the current user.
   *
   * Never rejects. On failure, `userAuth.status` becomes 'unauthenticated'
   * and `userAuth.error` is set, but not until the next render, so do not
   * read `userAuth` immediately after awaiting this. React to it in a
   * useEffect keyed on `userAuth`.
   *
   * Possible values of `userAuth.error`:
   *  * UserLoginCredentialsError
   *  * UserDeactivatedError
   *  * UserNotFoundError
   *  * UnexpectedError
   */
  const register = useCallback(async (registerDTO: RegisterDTO) => {
    try {
      providerLogger.ns('register').info('Now registering');
      setUserAuth({
        currentUser: null,
        status: 'loading'
      });
      await registerUser(config.registerPath, registerDTO);
<<<<<<< HEAD
      setUserAuth({
        currentUser: null,
        status: 'unauthenticated',
        error: null,
      });
=======

>>>>>>> origin/master
    } catch (err) {
      providerLogger.warn(`Unable to register: ${err}`);
      setUserAuth({
        currentUser: null,
        status: 'unauthenticated'
      });

      throw err
    }
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const user = await fetchUser(config.fetchUserPath);
        if (!cancelled)
          setUserAuth({
            currentUser: user,
            status: 'authenticated'
          });
      } catch (err) {
        if (!cancelled) {
          providerLogger.warn(`Unable to fetch user on load: ${err}`);
          setUserAuth({
            currentUser: null,
            status: 'unauthenticated'
          });
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const onUnauthorized = () => {
      setUserAuth({
        currentUser: null,
        status: 'unauthenticated'
      });
    };
    window.addEventListener(eventNames.UNAUTHORIZED, onUnauthorized);
    return () =>
      window.removeEventListener(eventNames.UNAUTHORIZED, onUnauthorized);
  }, []);

  const value = useMemo(
    () => ({
      userAuth,
      login,
      logout,
      register,
    }),
    [userAuth, login, logout, register],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx)
    throw new UnexpectedError('useAuth must be used within an AuthProvider.');
  return ctx;
}
