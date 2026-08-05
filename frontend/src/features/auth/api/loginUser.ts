import { UnexpectedError } from '@/errors/UnexpectedError';
import netquest from '@/utils/netquest';

import { logger } from '@/utils/utils';
import { UserLoginCredentialsError } from '../errors/UserLoginCredentialsError';
import { UserDeactivatedError } from '../errors/UserDeactivatedError';
import type { LoginDTO } from '../types/LoginDTO';

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
    const response = await netquest.post(url, {
      body: {
        ...loginDTO,
      },
      skipErrorEvent: true,
    });
    if (response.status != 200) {
      mainLogger.fail('User login failed.');
      if (response.status === 400) {
        mainLogger.warn('Invalid credentials provided.');
        throw new UserLoginCredentialsError();
      } else if (response.status === 409) {
        mainLogger.warn('User is already deactivated.');
        throw new UserDeactivatedError();
      } else if (response.status >= 200 && response.status < 300) {
        mainLogger.warn(
          `Unexpected ${response.status} level status code returned by server`,
        );
      } else {
        mainLogger.error(`Unexpected error code returned by server.`);
        mainLogger.debug(`Error code is ${response.status}`);
        throw new UnexpectedError(
          `Unexpected response status (${response.status}) during login`,
        );
      }
    }
    mainLogger.success('Successfully fetched user');
  } catch (error) {
    mainLogger.error('Failed to login user.');
    mainLogger.verbose(`Error: ${String(error)}`);
    throw new UnexpectedError(
      `An unexpected error occurred while trying to login: ${String(error)}`,
    );
  }
}
