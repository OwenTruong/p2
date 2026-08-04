import { StatusError } from './errors';
import { logger } from './utils';

const fileLogger = logger.ns('netquest').seal();

async function get(
  url: string,
  options?: {
    params?: Record<string, string>;
    headers?: Record<string, string>;
  },
): Promise<Response> {
  const { params, headers } = options || {};
  let fullURL = url;
  if (params) {
    const queryString = new URLSearchParams(params).toString();
    fullURL += `?${queryString}`;
  }

  fileLogger.ns('get').debug(`URL to Request: ${fullURL}`);

  try {
    const res = await fetch(fullURL, {
      method: 'GET',
      headers: {
        ...(headers || {}),
      },
    });
    fileLogger.ns('get').debug(`Response Code: ${res.status}`);
    fileLogger.ns('get').verbose(`Response Body: ${res.body ?? 'null'}`);
    if (!res.ok) {
      throw new StatusError(res.status.toString(), res.statusText);
    }
    return res;
  } catch (err: unknown) {
    fileLogger
      .ns('get')
      .fail(`Request failed with the following error: ${String(err)}`);
    throw err;
  }
}

async function post(
  url: string,
  options?: {
    params?: Record<string, string>;
    headers?: Record<string, string>;
    body?: Record<string, unknown>;
  },
): Promise<Response> {
  const { params, headers, body } = options || {};
  let fullURL = url;
  if (params) {
    const queryString = new URLSearchParams(params).toString();
    fullURL += `?${queryString}`;
  }

  fileLogger.ns('post').debug(`URL to Request: ${fullURL}`);

  try {
    const res = await fetch(fullURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(headers || {}),
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    fileLogger.ns('post').debug(`Response Code: ${res.status}`);
    fileLogger.ns('post').verbose(`Response Body: ${res.body ?? 'null'}`);

    if (!res.ok) {
      throw new StatusError(res.status.toString(), res.statusText);
    }
    return res;
  } catch (err: unknown) {
    fileLogger
      .ns('post')
      .fail(`Request failed with the following error: ${String(err)}`);
    throw err;
  }
}

export default { get, post };
