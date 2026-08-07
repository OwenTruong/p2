import z from "zod";

export interface LoginDTO {
  email: string;
  password: string;
}

export const LoginDTOSchema = z.object({
  email: z.email(),
  password: z.string().nonempty(),
}) satisfies z.ZodType<LoginDTO>;
