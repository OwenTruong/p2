import { StatusError } from '@/errors/StatusError';
import { logger, mode } from './utils';

const fileLogger = logger.ns('netquest').seal();

export const eventNames = {
  BAD_REQUEST: 'netquest:badRequest',
  UNAUTHORIZED: 'netquest:unauthorized',
  FORBIDDEN: 'netquest:forbidden',
  DEFAULT: 'netquest:default',
} as const;

export type NetquestEventName = (typeof eventNames)[keyof typeof eventNames];

export type NetquestErrorDetail = {
  status: number;
  url: string;
  statusText: string;
};

const statusEventMap: Record<number, NetquestEventName> = {
  400: eventNames.BAD_REQUEST,
  401: eventNames.UNAUTHORIZED,
  403: eventNames.FORBIDDEN,
};

function dispatchBadStatus(detail: NetquestErrorDetail) {
  const eventName = statusEventMap[detail.status] ?? eventNames.DEFAULT;
  window.dispatchEvent(
    new CustomEvent<NetquestErrorDetail>(eventName, { detail }),
  );
}

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export type RequestOptions = {
  params?: Record<string, string>;
  headers?: Record<string, string>;
  body?: Record<string, unknown>;
  /** Suppress the window event for expected failures (e.g. bad login creds). */
  skipErrorEvent?: boolean;
  signal?: AbortSignal;
};

/** Buffers the body for logging only. Never let this break a request. */
async function safeBodyPreview(res: Response): Promise<string> {
  if (mode === 'production') return '(not logged in production)';
  try {
    const text = await res.clone().text();
    return text || '(empty)';
  } catch {
    return '(unreadable)';
  }
}

async function request(
  method: HttpMethod,
  url: string,
  options: RequestOptions = {},
): Promise<Response> {
  const { params, headers, body, skipErrorEvent, signal } = options;
  const log = fileLogger.ns(method.toLowerCase());

  const fullURL = params
    ? `${url}?${new URLSearchParams(params).toString()}`
    : url;

  log.debug(`URL to Request: ${fullURL}`);

  let res: Response;
  try {
    res = await fetch(fullURL, {
      method,
      credentials: 'include',
      headers: {
        ...(body ? { 'Content-Type': 'application/json' } : {}),
        ...(headers ?? {}),
      },
      body: body ? JSON.stringify(body) : undefined,
      signal,
    });
  } catch (err: unknown) {
    // Only genuine transport failures reach here: DNS, offline, CORS, abort.
    log.fail(`Network request failed: ${String(err)}`);
    throw err;
  }

  log.debug(`Response Code: ${res.status}`);
  log.verbose(`Response Body: ${await safeBodyPreview(res)}`);

  if (!res.ok) {
    log.fail(`Request rejected: ${res.status} ${res.statusText}`);
    const detail: NetquestErrorDetail = {
      status: res.status,
      url: fullURL,
      statusText: res.statusText,
    };
    if (!skipErrorEvent) dispatchBadStatus(detail);
    throw new StatusError(res.status.toString(), res.statusText);
  }

  return res;
}

function get(url: string, options?: Omit<RequestOptions, 'body'>) {
  return request('GET', url, options);
}

function post(url: string, options?: RequestOptions) {
  return request('POST', url, options);
}

function put(url: string, options?: RequestOptions) {
  return request('PUT', url, options);
}

export default { get, post, put };
