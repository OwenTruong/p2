import { type User } from './User';

export interface UserAuth {
  currentUser: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: Error | null;
}
