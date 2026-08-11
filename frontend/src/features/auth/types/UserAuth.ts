import z from "zod";

import { type User, UserSchema } from "./User";

export interface UserAuth {
  currentUser: User | null;
  status: "authenticated" | "unauthenticated" | "loading";
}

export const UserAuthSchema = z.object({
  currentUser: UserSchema.nullable(),
  status: z.literal(["authenticated", "unauthenticated", "loading"]),
  error: z.instanceof(Error).nullable(),
}) satisfies z.ZodType<UserAuth>;
