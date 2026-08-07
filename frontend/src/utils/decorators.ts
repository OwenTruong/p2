import adze from "adze";
import { UnexpectedError } from "@/errors/UnexpectedError";

export function safeBind<Args extends unknown[], Return>(
  targetFunction: (...args: Args) => Promise<Return>,
  logger: adze<string, unknown>,
  {
    cleanup,
    handleError,
  }: {
    cleanup?: (
      args: Args,
      logger: adze<string, unknown>,
    ) => Promise<void> | void;
    handleError?: (
      args: Args,
      error: Error,
      logger: adze<string, unknown>,
    ) => Promise<Return> | Return;
  } = {},
): (...args: Args) => Promise<Return> {
  return async (...args: Args) => {
    try {
      return await targetFunction(...args);
    } catch (error: unknown) {
      if (!(error instanceof Error)) {
        const funcName = targetFunction.name || "anonymousFunction";

        logger.error(`Failed to run ${funcName}`);
        logger.verbose(`Error: ${error}`);
        throw new UnexpectedError(`Failed to run ${funcName}`);
      } else {
        if (handleError) {
          return await handleError(args, error, logger);
        } else {
          throw error;
        }
      }
    } finally {
      if (cleanup) {
        await cleanup(args, logger);
      }
    }
  };
}

export function ErrorHandler<This, Args extends unknown[], Return>(
  logger: adze<string, unknown>,
  handleError?: (
    args: Args,
    error: Error,
    logger: adze<string, unknown>,
  ) => Promise<Return>,
) {
  function decorator(
    originalMethod: (this: This, ...args: Args) => Promise<Return>,
    _context: ClassMethodDecoratorContext<
      This,
      (this: This, ...args: Args) => Promise<Return>
    >,
  ) {
    async function replacementMethod(
      this: This,
      ...args: Args
    ): Promise<Return> {
      try {
        return await originalMethod.call(this, ...args);
      } catch (error: unknown) {
        if (!(error instanceof Error)) {
          const methodName = `${(this as { constructor: { name: string } }).constructor.name}.${String(_context.name)}`;
          logger.error(`Failed to run ${methodName}`);
          logger.verbose(`Error: ${error}`);
          throw new UnexpectedError(`Failed to run ${methodName}`);
        }

        if (handleError) return await handleError(args, error, logger);
        throw error;
      }
    }
    return replacementMethod;
  }

  return decorator;
}

export function LogPositionalArgs<This, Args extends unknown[], Return>(
  logger: adze<string, unknown>,
  argsToLog: number[],
) {
  function decorator(
    originalMethod: (this: This, ...args: Args) => Return,
    _context: ClassMethodDecoratorContext<
      This,
      (this: This, ...args: Args) => Return
    >,
  ) {
    function replacementMethod(this: This, ...args: Args): Return {
      const methodName = `${(this as { constructor: { name: string } }).constructor.name}.${String(_context.name)}`;

      logger.info(`Entering ${methodName}`);
      logger.debug(
        `Entering ${methodName} with args ${args.filter((_el, i) => argsToLog.includes(i)).toString()}`,
      );
      return originalMethod.call(this, ...args);
    }
    return replacementMethod;
  }

  return decorator;
}

export function Retry<This, Args extends unknown[], Return>(
  logger: adze<string, unknown>,
  retryCount: number,
) {
  function decorator(
    originalMethod: (this: This, ...args: Args) => Promise<Return> | Return,
    _context: ClassMethodDecoratorContext<
      This,
      (this: This, ...args: Args) => Promise<Return> | Return
    >,
  ) {
    async function replacementMethod(
      this: This,
      ...args: Args
    ): Promise<Return> {
      let error: Error | null = null;
      for (let i = 0; i < retryCount; i++) {
        try {
          return await originalMethod.call(this, ...args);
        } catch (err: unknown) {
          const funcName = originalMethod.name || "anonymousFunction";
          const isLastAttempt = i + 1 === retryCount;

          if (!(err instanceof Error)) {
            logger.error(
              `Failed to run ${funcName}${isLastAttempt ? "" : ". Retrying..."}`,
            );
            logger.verbose(`Error: ${err}`);
            error = new UnexpectedError(`Failed to run ${funcName}`);
          } else {
            logger.error(
              `Failed to run ${funcName}${isLastAttempt ? "" : ". Retrying..."}`,
            );
            logger.verbose(`Error: ${err.message}`);
            error = err;
          }
        }
      }
      throw error;
    }
    return replacementMethod;
  }
  return decorator;
}
