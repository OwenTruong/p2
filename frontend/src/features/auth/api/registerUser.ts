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
      if (axios.isAxiosError<ApiErrorResponse>(error) && error.response) {
          throw new RegistrationError(
            error.response.status,
            error.response.data
          );
      }

      throw error;
  }


}