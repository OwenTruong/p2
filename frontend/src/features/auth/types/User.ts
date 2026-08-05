import z from 'zod';

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  status: 'Active';
}

export const UserSchema = z.object({
  id: z.string().nonempty(),
  email: z.email(),
  first_name: z.string().nonempty(),
  last_name: z.string().nonempty(),
  status: z.literal(['Active'], { error: 'User status is not active' }),
}) satisfies z.ZodType<User>;
