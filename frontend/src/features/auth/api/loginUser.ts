import { UnexpectedError } from '@/errors/UnexpectedError';
import netquest from '@/utils/netquest';

import { logger } from '@/utils/utils';
import { UserLoginCredentialsError } from '../errors/UserLoginCredentialsError';
import { UserDeactivatedError } from '../errors/UserDeactivatedError';
import type { LoginDTO } from '../types/LoginDTO';
import { StatusError } from '@/errors/StatusError';

const fileLogger = logger.ns('auth').seal();
const mainLogger = fileLogger.ns('loginUser').seal();

/**
 *
 * @param {string} url
 * @param {LoginDTO} loginDTO
 *
 * @throws {UserLoginCredentialsError}
 * @throws {UserDeactivatedError}
 * @throws {UnexpectedError}
 */
export async function loginUser(
  url: string,
  loginDTO: LoginDTO,
): Promise<void> {
  try {
    mainLogger.info(`Now sending a loginUser request to ${url}`);
    const response = await netquest.post(url, {
      body: {
        ...loginDTO,
      },
      skipErrorEvent: true,
    });
    if (response.status != 200) {
      mainLogger.fail('User login failed.');
      if (response.status >= 200 && response.status < 300) {
        mainLogger.warn(
          `Unexpected ${response.status} level status code returned by server`,
        );
      }
    }
    mainLogger.success('Successfully fetched user');
  } catch (error) {
    if (error instanceof StatusError) {
      const status = Number(error.code);
      // FIXME: For some reason, our architecture and backend is returning 401 for invalid email/password
      if (status === 401 || status === 422) {
        mainLogger.warn('Invalid credentials provided.');
        throw new UserLoginCredentialsError();
      } else if (status === 409) {
        mainLogger.warn('User is already deactivated.');
        throw new UserDeactivatedError();
      } else {
        mainLogger.error(`Unexpected error code returned by server.`);
        mainLogger.debug(`Error code is ${status}`);

        throw new UnexpectedError(
          `Unexpected response status (${status}) during login`,
        );
      }
    } else if (
      error instanceof UserLoginCredentialsError ||
      error instanceof UserDeactivatedError ||
      error instanceof UnexpectedError
    ) {
      throw error;
    } else {
      mainLogger.error('Failed to login user.');
      mainLogger.verbose(error);
      throw new UnexpectedError(
        `An unexpected error occurred while trying to login: ${String(error)}`,
      );
    }
  }
}
