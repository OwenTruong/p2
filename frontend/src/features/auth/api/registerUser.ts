<<<<<<< HEAD
import { UnexpectedError } from '@/errors/UnexpectedError';
import netquest from '@/utils/netquest';

import { logger } from '@/utils/utils';
import { UserLoginCredentialsError } from '../errors/UserLoginCredentialsError';
import type { RegisterDTO } from '../types/RegisterDTO';
import { StatusError } from '@/errors/StatusError';

const fileLogger = logger.ns('auth').seal();
const mainLogger = fileLogger.ns('registerUser').seal();
=======
// import { UnexpectedError } from "@/errors/UnexpectedError";
// import netquest from "@/utils/netquest";

// import { logger } from "@/utils/utils";
import type { RegisterDTO, RegisterResponseDTO } from "../types/RegisterDTO";
import axios from "axios";
import { RegistrationError } from "../errors/RegistrationError";
import type { ApiErrorResponse } from "@/errors/ApiError";

const api = axios.create({
  baseURL: "http://localhost:8010/api",
  withCredentials: true,
});
// const fileLogger = logger.ns("auth").seal();
// const mainLogger = fileLogger.ns("registerUser").seal();
>>>>>>> origin/master

/**
 *
 * @param {string} url
 * @param {RegisterDTO} registerDTO
 * 
 */
export async function registerUser(
  url: string,
  registerDTO: RegisterDTO,
<<<<<<< HEAD
): Promise<void> {
  try {
    mainLogger.info(`Now sending a registerUser request to ${url}`);
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
    mainLogger.success('Successfully registered user');
  } catch (error) {
    if (error instanceof StatusError) {
      const status = Number(error.code);
      if (status === 400 || status === 409 || status === 422) {
        mainLogger.debug(error);
        throw new UserLoginCredentialsError();
      } else {
        mainLogger.error(`Unexpected error code returned by server.`);
        mainLogger.debug(`Error code is ${status}`);
        throw new UnexpectedError(
          `Unexpected response status (${status}) during login`,
        );
=======
): Promise<RegisterResponseDTO> {

  console.log(url)

  try {
    const response = await api.post<RegisterResponseDTO>(
      "/auth/register",
      registerDTO,
    );
    return response.data;

  } catch (error) {
      if (axios.isAxiosError<ApiErrorResponse>(error) && error.response) {
          throw new RegistrationError(
            error.response.status,
            error.response.data
          );
>>>>>>> origin/master
      }

      throw error;
<<<<<<< HEAD
    } else {
      mainLogger.error('Failed to register user.');
      mainLogger.verbose(error);
      throw new UnexpectedError(
        `An unexpected error occurred while trying to register: ${String(error)}`,
      );
    }
=======
>>>>>>> origin/master
  }


}