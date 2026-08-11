import { ApiError, type ApiErrorResponse } from "@/errors/ApiError";

export class LoginError extends ApiError {
  constructor(status: number, response: ApiErrorResponse) {
    super(status, response);
    this.name = "LoginError";
  }
}