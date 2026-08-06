import { StatusError } from "@/errors/StatusError";
import { UnexpectedError } from "@/errors/UnexpectedError";
import netquest from "@/utils/netquest";

import { logger } from "@/utils/utils";

const fileLogger = logger.ns("auth").seal();
const mainLogger = fileLogger.ns("loginUser").seal();

/**
 *
 * @param {string} url
 *
 * @throws {UnexpectedError}
 */
export async function logoutUser(url: string): Promise<void> {
  try {
    mainLogger.info(`Now sending a logoutUser request to ${url}`);
    const response = await netquest.post(url, { skipErrorEvent: true });
    if (response.status != 200) {
      mainLogger.fail("User logout failed.");
      if (response.status >= 200 && response.status < 300) {
        mainLogger.warn(
          `Unexpected ${response.status} level status code returned by server`,
        );
      }
    }
    mainLogger.success("Successfully logged out user.");
  } catch (error) {
    if (error instanceof StatusError) {
      mainLogger.error(`Unexpected error code returned by server.`);
      mainLogger.debug(`Error code is ${error.code}`);
      throw new UnexpectedError(
        `Unexpected response status (${error.code}) during login`,
      );
    } else if (error instanceof UnexpectedError) {
      throw error;
    } else {
      mainLogger.error("Failed to log out user.");
      mainLogger.verbose(error);
      throw new UnexpectedError(
        `An unexpected error occurred while trying to logout: ${String(error)}`,
      );
    }
  }
}
