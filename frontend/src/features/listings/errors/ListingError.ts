import { ApiError, type ApiErrorResponse } from "@/errors/ApiError";

export class ListingError extends ApiError {
  constructor(status: number, response: ApiErrorResponse) {
    super(status, response);
    this.name = "ListingError";
  }
}