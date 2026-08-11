export type ApiErrorItem = {
  message: string;
};

export type ApiErrorResponse = {
    errors: {
        message: string;
    }[];
};

export class RegistrationError extends Error {
  readonly errors: ApiErrorItem[];

  constructor(errors: ApiErrorItem[]) {
    super(errors[0]?.message ?? "Unable to register user.");
    this.name = "RegistrationError";
    this.errors = errors;
  }
}

export class LoginError extends Error {
  readonly errors: ApiErrorItem[];

  constructor(errors: ApiErrorItem[]) {
    super(errors[0]?.message ?? "Unable to login.");
    this.name = "LoginError";
    this.errors = errors
  }
}