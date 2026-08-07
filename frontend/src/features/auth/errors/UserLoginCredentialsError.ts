export class UserLoginCredentialsError extends Error {
  constructor(message: string = "Invalid email and password provided.") {
    super(message);
    this.name = "UserLoginCredentialsError";
  }
}
