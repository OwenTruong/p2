import z from 'zod';

export interface User {
  id: string;
  email: string;
}

export const UserSchema = z.object({
  id: z.string(),
  email: z.email(),
});
