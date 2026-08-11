import adze, { setup } from "adze";

function getMode(): "development" | "production" | "preview" {
  const mode = import.meta.env.VITE_MODE;

  if (mode === "development" || mode === "production" || mode === "preview") {
    return mode;
  }

  console.error("MODE is not set correctly:", mode);

  return "production";
}

export const mode = getMode();
export const isDev = getMode() === "development";
export const isPreview = getMode() === "preview";
export const isProd = getMode() === "production";

setup({
  activeLevel: mode === "production" ? "info" : "verbose",
});

export const logger = adze.withEmoji.timestamp.seal();

logger.info(`Mode is set to ${mode}`);
