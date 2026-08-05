import { UnexpectedError } from '@/errors/UnexpectedError';
import netquest from '@/utils/netquest';

import { logger } from '@/utils/utils';
import { UserLoginCredentialsError } from '../errors/UserLoginCredentialsError';
import type { RegisterDTO } from '../types/RegisterDTO';

const fileLogger = logger.ns('auth').seal();
const mainLogger = fileLogger.ns('registerUser').seal();

/**
 *
 * @param {string} url
 * @param {RegisterDTO} registerDTO
 *
 * @throws {UserLoginCredentialsError}
 * @throws {UnexpectedError}
 */
export async function registerUser(
  url: string,
  registerDTO: RegisterDTO,
): Promise<void> {
  try {
    const response = await netquest.post(url, {
      body: {
        ...registerDTO,
      },
      skipErrorEvent: true,
    });
    if (response.status != 201) {
      mainLogger.fail('User registration failed.');
      if (response.status === 400 || response.status === 409) {
        mainLogger.warn('Invalid credentials provided.');
        throw new UserLoginCredentialsError();
      } else if (response.status >= 200 && response.status < 300) {
        mainLogger.warn(
          `Unexpected ${response.status} level status code returned by server`,
        );
      } else {
        mainLogger.error(`Unexpected error code returned by server.`);
        mainLogger.debug(`Error code is ${response.status}`);
        throw new UnexpectedError(
          `Unexpected response status (${response.status}) during registration`,
        );
      }
    }

    const result = await response.json();
    mainLogger.success('Su');
  } catch (error) {
    mainLogger.error('Failed to register user.');
    mainLogger.verbose(`Error: ${String(error)}`);
    throw new UnexpectedError(
      `An unexpected error occurred while trying to register: ${String(error)}`,
    );
  }
}
