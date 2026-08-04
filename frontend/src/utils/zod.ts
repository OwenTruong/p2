import * as z from 'zod';

// ==========================================
// Core Validation Helper
// ==========================================

export function validate<T>(schema: z.ZodType<T>, input: unknown): input is T {
  const result = schema.safeParse(input);
  if (!result.success) {
    console.error('Validation failed:', result.error.flatten());
  }
  return result.success;
}

export function parseOrThrow<T>(schema: z.ZodType<T>, input: unknown): T {
  return schema.parse(input);
}

export function safeParseResult<T>(schema: z.ZodType<T>, input: unknown) {
  return schema.safeParse(input);
}

// ==========================================
// Common Helpers
// ==========================================

export const NoWhitespaceSchema = z.string().refine(
  (str) => {
    const regex = /^\s|\s$/;
    return regex.test(str) != true;
  },
  {
    error: `No leading or trailing whitespace allowed`,
  },
);
