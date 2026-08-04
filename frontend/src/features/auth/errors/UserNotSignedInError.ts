export class UserNotSignedInError extends Error {
  constructor(message: string = 'User is not signed in') {
    super(message);
    this.name = 'UserNotSignedInError';
  }
}
