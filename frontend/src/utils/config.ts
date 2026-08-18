import { logger } from "./utils";

const fileLogger = logger.ns("config").seal();

function joinPaths(path1: string, path2: string) {
  // Handles trailing slashes
  return `${path1.replace(/\/$/, "")}/${path2.replace(/^\//, "")}`;
}

const authServiceUrl: string =
  import.meta.env.VITE_AUTH_SERVICE_URL ?? "http://10.0.0.1:8080";
const listingServiceUrl: string = import.meta.env.VITE_LISTING_SERVICE_URL ?? 'http://10.0.0.1:8080';
// const reservationServiceUrl: string = import.meta.env.VITE_RESERVATION_SERVICE_URL ?? 'http://10.0.0.1:8080';
// const sampleServiceUrl: string = import.meta.env.VITE_SAMPLE_SERVICE_URL ?? 'http://10.0.0.1:8080';

export const loginPath = joinPaths(authServiceUrl, "/api/auth/login");
export const logoutPath = joinPaths(authServiceUrl, "/api/auth/logout");
export const registerPath = joinPaths(authServiceUrl, "/api/auth/register");
export const fetchUserPath = joinPaths(authServiceUrl, "/api/users/me");

export const getListingsPath = joinPaths(listingServiceUrl, "/api/listings/me")
export const config = {
  loginPath,
  logoutPath,
  registerPath,
  fetchUserPath,
};

fileLogger.info(config);
