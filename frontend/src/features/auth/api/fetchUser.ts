import netquest from '@/utils/netquest';

import { UnexpectedError } from '@/errors/UnexpectedError';
import { logger } from '@/utils/utils';
import { validate } from '@/utils/zod';

import { UserNotSignedInError } from '../errors/UserNotSignedInError';

import { type User, UserSchema } from '../types/User';
import { UserNotFoundError } from '../errors/UserNotFoundError';
import { StatusError } from '@/errors/StatusError';

const fileLogger = logger.ns('auth').seal();
const mainLogger = fileLogger.ns('fetchUser').seal();

/**
 *
 * @param {string} url
 * @returns {Promise<User>}
 * @throws {UserNotFoundError} If the user is not found (404)
 * @throws {UserNotSignedInError} If the user is not signed in (401)
 * @throws {UserDeactivatedError} If the user is deactivated
 * @throws {UnexpectedError} For any other unexpected errors
 */
export async function fetchUser(url: string): Promise<User> {
  try {
    mainLogger.info(`Now sending a fetchUser request to ${url}`);
    const userResponse = await netquest.get(url, { skipErrorEvent: true });
    if (userResponse.status != 200) {
      mainLogger.fail('User fetching failed.');
      if (!(userResponse.status >= 200 && userResponse.status < 300)) {
        mainLogger.error(`Unexpected error code returned by server.`);
        mainLogger.debug(`Error code is ${userResponse.status}`);
        throw new UnexpectedError(
          `Unexpected response status (${userResponse.status}) when fetching email`,
        );
      }
    }
    const userResult = await userResponse.json();
    mainLogger.success('Successfully fetched user');

    if (validate<User>(UserSchema, userResult)) {
      return userResult;
    } else {
      // devLog('Invalid user format received from server:', userResult);
      mainLogger.error(`Invalid user format received from server.`);
      mainLogger.debug(`userResult: ${userResult}`);
      throw new UnexpectedError('Invalid user format received from server');
    }
  } catch (error) {
    if (error instanceof StatusError) {
      const status = Number(error.code);
      mainLogger.debug(`Registration rejected with ${status}`);
      if (status === 404) {
        mainLogger.warn(
          'User not found. If user has not logged in before yet, this function should not be called.',
        );
        throw new UserNotFoundError();
      } else if (status === 401) {
        mainLogger.warn(
          'User is not signed in. This function should not be called.',
        );
        throw new UserNotSignedInError();
      } else if (status === 400) {
        mainLogger.info('An invalid email was provided.');
        throw new UnexpectedError('Bad request when fetching email');
      } else if (status >= 500) {
        mainLogger.error(`Server error. Unable to fetch user.`);
        throw new UnexpectedError(
          `Server error (${status}) when fetching email`,
        );
      }
    }
    if (
      error instanceof UserNotFoundError ||
      error instanceof UserNotSignedInError ||
      error instanceof UnexpectedError
    ) {
      throw error;
    } else {
      mainLogger.error('Failed to fetch user successfully.');
      mainLogger.verbose(error);
      throw new UnexpectedError(
        `An unexpected error occurred while fetching email: ${String(error)}`,
      );
    }
  }
}
