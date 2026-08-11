import { ApiError, type ApiErrorResponse } from "@/errors/ApiError";

export class RegistrationError extends ApiError {
  constructor(status: number, response: ApiErrorResponse) {
    super(status, response);
    this.name = "RegistrationError";
  }
}