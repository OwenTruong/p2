// import { UnexpectedError } from "@/errors/UnexpectedError";
// import netquest from "@/utils/netquest";

// import { logger } from "@/utils/utils";
import type { RegisterDTO, RegisterResponseDTO } from "../types/RegisterDTO";
// import { RegistrationError, type ApiErrorResponse } from "../types/RegistrationError";
import axios from "axios";
import { RegistrationError, type ApiErrorResponse } from "../types/RegistrationError";

const api = axios.create({
  baseURL: "http://localhost:8010/api",
  withCredentials: true,
});
// const fileLogger = logger.ns("auth").seal();
// const mainLogger = fileLogger.ns("registerUser").seal();

/**
 *
 * @param {string} url
 * @param {RegisterDTO} registerDTO
 * 
 */
export async function registerUser(
  url: string,
  registerDTO: RegisterDTO,
): Promise<RegisterResponseDTO> {

  console.log(url)

  try {
    const response = await api.post<RegisterResponseDTO>(
      "/auth/register",
      registerDTO,
    );
    return response.data;

  } catch (error) {
      if (axios.isAxiosError<ApiErrorResponse>(error)) {
          const apiErrors = error.response?.data.errors;
          throw new RegistrationError(apiErrors ?? []);
      }

      throw error;
  }


}