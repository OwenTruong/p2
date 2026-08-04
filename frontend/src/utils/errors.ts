import z from 'zod';

export class StatusError extends Error {
  code: string;

  constructor(code: string, message: string) {
    super(message);
    if (
      z
        .looseObject({
          code: z.string().min(1),
          message: z.string(),
        })
        .safeParse({
          code,
          message,
        }).success
    ) {
      this.code = code;
    } else {
      throw new Error('Internal Error: Invalid StatusError parameters');
    }
  }
}

export class UnexpectedError extends Error {
  constructor(message?: string) {
    super(message);
    this.name = 'UnexpectedError';
  }
}
