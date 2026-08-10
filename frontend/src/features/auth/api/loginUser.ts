// import { UnexpectedError } from "@/errors/UnexpectedError";
// import netquest from "@/utils/netquest";

// import { logger } from "@/utils/utils";
// import { UserLoginCredentialsError } from "../errors/UserLoginCredentialsError";
// import { UserDeactivatedError } from "../errors/UserDeactivatedError";
import type { LoginDTO } from "../types/LoginDTO";
// import { StatusError } from "@/errors/StatusError";
import axios from "axios";
import { LoginError } from "../types/RegistrationError";

// const fileLogger = logger.ns("auth").seal();
// const mainLogger = fileLogger.ns("loginUser").seal();

const api = axios.create({
  baseURL: "http://localhost:8010/api",
  withCredentials: true,
});

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

  console.log(url)
  
  try {
    const response = await api.post(
      "/auth/login",
      loginDTO
    );

    return response.data

  } catch (error) {
    if (axios.isAxiosError(error)) {
      const apiErrors = error.response?.data.errors;
      throw new LoginError(apiErrors ?? []);
    }
  }
}
