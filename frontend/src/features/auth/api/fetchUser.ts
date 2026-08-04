import netquest from '@/utils/netquest';

import { UnexpectedError } from '@/errors/UnexpectedError';
import { logger } from '@/utils/utils';
import { validate } from '@/utils/zod';

import { UserNotSignedInError } from '../errors/UserNotSignedInError';

import { type User, UserSchema } from '../types/User';
import { UserNotFoundError } from '../errors/UserNotFoundError';

const fileLogger = logger.ns('userInfo').seal();
const fetchUserLogger = fileLogger.ns('fetchUser').seal();

/**
 *
 * @param {string} url
 * @returns {Promise<User>}
 * @throws {UserNotFoundError} If the user is not found (404)
 * @throws {UserNotSignedInError} If the user is not signed in (401)
 * @throws {UnexpectedError} For any other unexpected errors
 */
export async function fetchUser(url: string): Promise<User> {
  try {
    const userResponse = await netquest.get(url);
    if (userResponse.status != 200) {
      fetchUserLogger.fail('User fetching failed.');
      if (userResponse.status === 404) {
        fetchUserLogger.warn(
          'User not found. If user has not logged in before yet, this function should not be called.',
        );
        throw new UserNotFoundError();
      } else if (userResponse.status === 401) {
        fetchUserLogger.warn(
          'User is not signed in. This functiono should not be called.',
        );
        throw new UserNotSignedInError();
      } else if (userResponse.status === 400) {
        fetchUserLogger.info('An invalid email was provided.');
        throw new UnexpectedError('Bad request when fetching email');
      } else if (userResponse.status >= 500) {
        fetchUserLogger.error(`Server error. Unable to fetch user.`);
        throw new UnexpectedError(
          `Server error (${userResponse.status}) when fetching email`,
        );
      } else if (!(userResponse.status >= 200 && userResponse.status < 300)) {
        fetchUserLogger.error(`Unexpected error code returned by server.`);
        fetchUserLogger.debug(`Error code is ${userResponse.status}`);
        throw new UnexpectedError(
          `Unexpected response status (${userResponse.status}) when fetching email`,
        );
      }
    }
    const userResult = await userResponse.json();
    fetchUserLogger.success('Successfully fetched user');

    if (validate<User>(UserSchema, userResult)) {
      return userResult;
    } else {
      // devLog('Invalid user format received from server:', userResult);
      fetchUserLogger.error(`Invalid user format received from server.`);
      fetchUserLogger.debug(`userResult: ${userResult}`);
      throw new UnexpectedError('Invalid user format received from server');
    }
  } catch (error) {
    if (
      error instanceof UserNotFoundError ||
      error instanceof UserNotSignedInError ||
      error instanceof UnexpectedError
    ) {
      throw error;
    } else {
      fetchUserLogger.error('Failed to fetch user successfully.');
      fetchUserLogger.verbose(`Error: ${String(error)}`);
      throw new UnexpectedError(
        `An unexpected error occurred while fetching email: ${String(error)}`,
      );
    }
  }
}
