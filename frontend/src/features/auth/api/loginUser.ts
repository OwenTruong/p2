// import { UnexpectedError } from "@/errors/UnexpectedError";
// import netquest from "@/utils/netquest";

// import { logger } from "@/utils/utils";
// import { UserLoginCredentialsError } from "../errors/UserLoginCredentialsError";
// import { UserDeactivatedError } from "../errors/UserDeactivatedError";
import { getAxios } from "@/utils/axios";
import { LoginError } from "../errors/LoginError";
import type { LoginDTO } from "../types/LoginDTO";
import axios from "axios";
// import { StatusError } from "@/errors/StatusError";

// const fileLogger = logger.ns("auth").seal();
// const mainLogger = fileLogger.ns("loginUser").seal();


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

    const response = await getAxios().post(
      url,
      loginDTO
    );

    return response.data

  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new LoginError(
        error.response.status,
        error.response.data
      );
    }
  }
}
