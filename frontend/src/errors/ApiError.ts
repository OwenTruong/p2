export type ApiErrorItem = {
  message: string;
};

export type ApiErrorResponse = {
    errors: ApiErrorItem[];
};

export class ApiError extends Error {
    readonly errors: ApiErrorItem[];
    readonly status: number;

    constructor(
        status: number,
        response: ApiErrorResponse
    ) {
        super(response.errors[0]?.message ?? "API request failed.");

        this.name = "ApiError";
        this.status = status;
        this.errors = response.errors;
    }
}