import z from 'zod';

export interface RegisterDTO {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export const RegisterDTOSchema = z.object({
  email: z.email(),
  password: z.string().nonempty(),
  first_name: z.string().nonempty(),
  last_name: z.string().nonempty(),
}) satisfies z.ZodType<RegisterDTO>;
