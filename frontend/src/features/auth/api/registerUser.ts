import { UnexpectedError } from '@/errors/UnexpectedError';
import netquest from '@/utils/netquest';

import { logger } from '@/utils/utils';
import { UserLoginCredentialsError } from '../errors/UserLoginCredentialsError';
import type { RegisterDTO } from '../types/RegisterDTO';
import { StatusError } from '@/errors/StatusError';

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
      if (response.status >= 200 && response.status < 300) {
        mainLogger.warn(
          `Unexpected ${response.status} level status code returned by server`,
        );
      }
    }

    await response.json();
    mainLogger.success('Successfully registered user');
  } catch (error) {
    if (error instanceof StatusError) {
      const status = Number(error.code);
      if (status === 400) {
        mainLogger.warn('Invalid credentials provided.');
        throw new UserLoginCredentialsError();
      } else if (status === 400 || status === 409 || status === 422) {
        mainLogger.debug(error);
        throw new UserLoginCredentialsError();
      } else {
        mainLogger.error(`Unexpected error code returned by server.`);
        mainLogger.debug(`Error code is ${status}`);
        throw new UnexpectedError(
          `Unexpected response status (${status}) during login`,
        );
      }
    } else if (
      error instanceof UserLoginCredentialsError ||
      error instanceof UnexpectedError
    ) {
      throw error;
    } else {
      mainLogger.error('Failed to register user.');
      mainLogger.verbose(error);
      throw new UnexpectedError(
        `An unexpected error occurred while trying to register: ${String(error)}`,
      );
    }
  }
}
