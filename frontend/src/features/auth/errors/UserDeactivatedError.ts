export class UserDeactivatedError extends Error {
  constructor(message: string = 'User has already been deactivated') {
    super(message);
    this.name = 'UserDeactivatedError';
  }
}
